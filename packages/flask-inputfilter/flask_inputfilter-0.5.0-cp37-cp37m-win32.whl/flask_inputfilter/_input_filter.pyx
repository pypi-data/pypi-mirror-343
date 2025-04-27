# cython: language=c++
# cython: language_level=3
# cython: binding=True
# cython: cdivision=True
# cython: boundscheck=False
# cython: initializedcheck=False
import json
import logging
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

from flask import Response, g, request

from flask_inputfilter.conditions import BaseCondition
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.filters import BaseFilter
from flask_inputfilter.mixins import ExternalApiMixin
from flask_inputfilter.models import ExternalApiConfig, FieldModel
from flask_inputfilter.validators import BaseValidator

from libcpp.string cimport string
from libcpp.vector cimport vector


cdef extern from "helper.h":
    vector[string] make_default_methods()

T = TypeVar("T")


cdef class InputFilter:
    """
    Base class for all input filters.
    """

    cdef readonly vector[string] methods
    cdef readonly dict fields
    cdef readonly list conditions
    cdef readonly list global_filters
    cdef readonly list global_validators
    cdef readonly dict data
    cdef readonly dict validated_data
    cdef readonly dict errors
    cdef readonly object model_class

    def __cinit__(self) -> None:
        self.methods = make_default_methods()
        self.fields: Dict[str, FieldModel] = {}
        self.conditions: List[BaseCondition] = []
        self.global_filters: List[BaseFilter] = []
        self.global_validators: List[BaseValidator] = []
        self.data: Dict[str, Any] = {}
        self.validated_data: Dict[str, Any] = {}
        self.errors: Dict[str, str] = {}
        self.model_class: Optional[Type[T]] = None

    def __init__(self, methods: Optional[List[str]] = None) -> None:
        if methods is not None:
            self.methods.clear()
            [self.methods.push_back(method.encode()) for method in methods]

    cpdef bint isValid(self):
        """
        Checks if the object's state or its attributes meet certain
        conditions to be considered valid. This function is typically used to
        ensure that the current state complies with specific requirements or
        rules.

        Returns:
            bool: Returns True if the state or attributes of the object fulfill
                all required conditions; otherwise, returns False.
        """
        try:
            self.validateData()

        except ValidationError as e:
            self.errors = e.args[0]
            return False

        return True

    @classmethod
    def validate(
        cls,
    ):
        """
        Decorator for validating input data in routes.

        Args:
            cls

        Returns:
            Callable[
                [Any],
                Callable[
                    [tuple[Any, ...], Dict[str, Any]],
                    Union[Response, tuple[Any, Dict[str, Any]]],
                ],
            ]
        """
        def decorator(
            f,
        ):
            """
            Decorator function to validate input data for a Flask route.

            Args:
                f (Callable): The Flask route function to be decorated.

            Returns:
                Callable[[Any, Any], Union[Response, tuple[Any, Dict[str, Any]]]]: The wrapped function with input validation.
            """

            def wrapper(
                *args, **kwargs
            ):
                """
                Wrapper function to handle input validation and
                error handling for the decorated route function.

                Args:
                    *args: Positional arguments for the route function.
                    **kwargs: Keyword arguments for the route function.

                Returns:
                    Union[Response, tuple[Any, Dict[str, Any]]]: The response from the route function or an error response.
                """

                cdef InputFilter input_filter = cls()
                cdef string request_method = request.method.encode()
                if not any(request_method == method for method in input_filter.methods):
                    return Response(status=405, response="Method Not Allowed")

                data = request.json if request.is_json else request.args

                try:
                    kwargs = kwargs or {}

                    input_filter.data = {**data, **kwargs}

                    g.validated_data = input_filter.validateData()

                except ValidationError as e:
                    return Response(
                        status=400,
                        response=json.dumps(e.args[0]),
                        mimetype="application/json",
                    )

                except Exception:
                    logging.getLogger(__name__).exception(
                        "An unexpected exception occurred while "
                        "validating input data.",
                    )
                    return Response(status=500)

                return f(*args, **kwargs)

            return wrapper

        return decorator

    cpdef object validateData(
        self, data: Optional[Dict[str, Any]] = None
    ):
        """
        Validates input data against defined field rules, including applying
        filters, validators, custom logic steps, and fallback mechanisms. The
        validation process also ensures the required fields are handled
        appropriately and conditions are checked after processing.

        Args:
            data (Dict[str, Any]): A dictionary containing the input data to
                be validated where keys represent field names and values
                represent the corresponding data.

        Returns:
            Union[Dict[str, Any], Type[T]]: A dictionary containing the validated data with
                any modifications, default values, or processed values as
                per the defined validation rules.

        Raises:
            Any errors raised during external API calls, validation, or
                logical steps execution of the respective fields or conditions
                will propagate without explicit handling here.
        """
        data = data or self.data
        cdef dict errors = {}
        cdef bint required
        cdef object default
        cdef object fallback
        cdef list filters
        cdef list validators
        cdef object external_api
        cdef str copy

        for field_name, field_info in self.fields.items():
            value = data.get(field_name)

            required = field_info.required
            default = field_info.default
            fallback = field_info.fallback
            filters = field_info.filters + self.global_filters
            validators = field_info.validators + self.global_validators
            steps = field_info.steps
            external_api = field_info.external_api
            copy = field_info.copy

            try:
                if copy:
                    value = self.validated_data.get(copy)

                if external_api:
                    value = ExternalApiMixin().callExternalApi(
                        external_api, fallback, self.validated_data
                    )

                value = self.applyFilters(filters, value)
                value = self.validateField(validators, fallback, value) or value
                value = self.applySteps(steps, fallback, value) or value
                value = InputFilter.checkForRequired(
                    field_name, required, default, fallback, value
                )

                self.validated_data[field_name] = value

            except ValidationError as e:
                errors[field_name] = str(e)

        try:
            self.checkConditions(self.conditions, self.validated_data)
        except ValidationError as e:
            errors["_condition"] = str(e)

        if errors:
            raise ValidationError(errors)

        if self.model_class is not None:
            return self.serialize()

        return self.validated_data

    cpdef void addCondition(self, condition: BaseCondition):
        """
        Add a condition to the input filter.

        Args:
            condition (BaseCondition): The condition to add.
        """
        self.conditions.append(condition)

    cpdef list getConditions(self):
        """
        Retrieve the list of all registered conditions.

        This function provides access to the conditions that have been
        registered and stored. Each condition in the returned list
        is represented as an instance of the BaseCondition type.

        Returns:
            List[BaseCondition]: A list containing all currently registered
                instances of BaseCondition.
        """
        return self.conditions

    cdef void checkConditions(self, conditions: List[BaseCondition], validated_data: Dict[str, Any]) except *:
        """
        Checks if all conditions are met.

        This method iterates through all registered conditions and checks
        if they are satisfied based on the provided validated data. If any
        condition is not met, a ValidationError is raised with an appropriate
        message indicating which condition failed.

        Args:
            conditions (List[BaseCondition]):
                A list of conditions to be checked against the validated data.
            validated_data (Dict[str, Any]):
                The validated data to check against the conditions.
        """
        for condition in conditions:
            if not condition.check(validated_data):
                raise ValidationError(
                    f"Condition '{condition.__class__.__name__}' not met."
                )

    cpdef void setData(self, data: Dict[str, Any]):
        """
        Filters and sets the provided data into the object's internal
        storage, ensuring that only the specified fields are considered and
        their values are processed through defined filters.

        Parameters:
            data (Dict[str, Any]):
                The input dictionary containing key-value pairs where keys
                represent field names and values represent the associated
                data to be filtered and stored.
        """
        self.data = {}
        for field_name, field_value in data.items():
            if field_name in self.fields:
                field_value = self.applyFilters(
                    filters=self.fields[field_name].filters + self.global_filters,
                    value=field_value,
                )

            self.data[field_name] = field_value

    cpdef object getValue(self, name: str):
        """
        This method retrieves a value associated with the provided name. It
        searches for the value based on the given identifier and returns the
        corresponding result. If no value is found, it typically returns a
        default or fallback output. The method aims to provide flexibility in
        retrieving data without explicitly specifying the details of the
        underlying implementation.

        Args:
            name (str): A string that represents the identifier for which the
                 corresponding value is being retrieved. It is used to perform
                 the lookup.

        Returns:
            Any: The retrieved value associated with the given name. The
                 specific type of this value is dependent on the
                 implementation and the data being accessed.
        """
        return self.validated_data.get(name)

    cpdef dict getValues(self):
        """
        Retrieves a dictionary of key-value pairs from the current object.
        This method provides access to the internal state or configuration of
        the object in a dictionary format, where keys are strings and values
        can be of various types depending on the object's design.

        Returns:
            Dict[str, Any]: A dictionary containing string keys and their
                            corresponding values of any data type.
        """
        return self.validated_data

    cpdef object getRawValue(self, name: str):
        """
        Fetches the raw value associated with the provided key.

        This method is used to retrieve the underlying value linked to the
        given key without applying any transformations or validations. It
        directly fetches the raw stored value and is typically used in
        scenarios where the raw data is needed for processing or debugging
        purposes.

        Args:
            name (str): The name of the key whose raw value is to be 
                retrieved.

        Returns:
            Any: The raw value associated with the provided key.
        """
        return self.data.get(name) if name in self.data else None

    cpdef dict getRawValues(self):
        """
        Retrieves raw values from a given source and returns them as a
        dictionary.

        This method is used to fetch and return unprocessed or raw data in
        the form of a dictionary where the keys are strings, representing
        the identifiers, and the values are of any data type.

        Returns:
            Dict[str, Any]: A dictionary containing the raw values retrieved.
               The keys are strings representing the identifiers, and the
               values can be of any type, depending on the source
               being accessed.
        """
        if not self.fields:
            return {}

        return {
            field: self.data[field]
            for field in self.fields
            if field in self.data
        }

    cpdef dict getUnfilteredData(self):
        """
        Fetches unfiltered data from the data source.

        This method retrieves data without any filtering, processing, or
        manipulations applied. It is intended to provide raw data that has
        not been altered since being retrieved from its source. The usage
        of this method should be limited to scenarios where unprocessed data
        is required, as it does not perform any validations or checks.

        Returns:
            Dict[str, Any]: The unfiltered, raw data retrieved from the
                 data source. The return type may vary based on the
                 specific implementation of the data source.
        """
        return self.data

    cpdef void setUnfilteredData(self, data: Dict[str, Any]):
        """
        Sets unfiltered data for the current instance. This method assigns a
        given dictionary of data to the instance for further processing. It
        updates the internal state using the provided data.

        Parameters:
            data (Dict[str, Any]): A dictionary containing the unfiltered
                data to be associated with the instance.
        """
        self.data = data

    def hasUnknown(self) -> bool:
        """
        Checks whether any values in the current data do not have
        corresponding configurations in the defined fields.

        Returns:
            bool: True if there are any unknown fields; False otherwise.
        """
        if not self.data and self.fields:
            return True

        return any(
            field_name not in self.fields.keys()
            for field_name in self.data.keys()
        )

    cpdef str getErrorMessage(self, field_name: str):
        """
        Retrieves and returns a predefined error message.

        This method is intended to provide a consistent error message
        to be used across the application when an error occurs. The
        message is predefined and does not accept any parameters.
        The exact content of the error message may vary based on
        specific implementation, but it is designed to convey meaningful
        information about the nature of an error.

        Args:
            field_name (str): The name of the field for which the error
                message is being retrieved.

        Returns:
            Optional[str]: A string representing the predefined error message.
        """
        return self.errors.get(field_name)

    cpdef dict getErrorMessages(self):
        """
        Retrieves all error messages associated with the fields in the
        input filter.

        This method aggregates and returns a dictionary of error messages
        where the keys represent field names, and the values are their
        respective error messages.

        Returns:
            Dict[str, str]: A dictionary containing field names as keys and
                            their corresponding error messages as values.
        """
        return self.errors

    cpdef void add(
        self,
        name: str,
        required: bool = False,
        default: Any = None,
        fallback: Any = None,
        filters: Optional[List[BaseFilter]] = None,
        validators: Optional[List[BaseValidator]] = None,
        steps: Optional[List[Union[BaseFilter, BaseValidator]]] = None,
        external_api: Optional[ExternalApiConfig] = None,
        copy: Optional[str] = None,
    ) except *:
        """
        Add the field to the input filter.

        Args:
            name (str): The name of the field.
            
            required (Optional[bool]): Whether the field is required.
            
            default (Optional[Any]): The default value of the field.
            
            fallback (Optional[Any]): The fallback value of the field, if 
                validations fails or field None, although it is required.
                
            filters (Optional[List[BaseFilter]]): The filters to apply to 
                the field value.
            
            validators (Optional[List[BaseValidator]]): The validators to 
                apply to the field value.
                
            steps (Optional[List[Union[BaseFilter, BaseValidator]]]): Allows 
                to apply multiple filters and validators in a specific order.
                
            external_api (Optional[ExternalApiConfig]): Configuration for an 
                external API call.
            
            copy (Optional[str]): The name of the field to copy the value 
                from.
        """
        if name in self.fields:
            raise ValueError(f"Field '{name}' already exists.")

        self.fields[name] = FieldModel(
            required=required,
            default=default,
            fallback=fallback,
            filters=filters or [],
            validators=validators or [],
            steps=steps or [],
            external_api=external_api,
            copy=copy,
        )

    cpdef bint has(self, field_name: str):
        """
        This method checks the existence of a specific field within the
        input filter values, identified by its field name. It does not return a
        value, serving purely as a validation or existence check mechanism.

        Args:
            field_name (str): The name of the field to check for existence.

        Returns:
            bool: True if the field exists in the input filter,
                otherwise False.
        """
        return field_name in self.fields

    cpdef object getInput(self, field_name: str):
        """
        Represents a method to retrieve a field by its name.

        This method allows fetching the configuration of a specific field
        within the object, using its name as a string. It ensures
        compatibility with various field names and provides a generic
        return type to accommodate different data types for the fields.

        Args:
            field_name (str): A string representing the name of the field who
                        needs to be retrieved.

        Returns:
            Optional[FieldModel]: The field corresponding to the
                specified name.
        """
        return self.fields.get(field_name)

    cpdef dict getInputs(self):
        """
        Retrieve the dictionary of input fields associated with the object.

        Returns:
            Dict[str, FieldModel]: Dictionary containing field names as
                keys and their corresponding FieldModel instances as values
        """
        return self.fields

    cpdef object remove(self, field_name: str):
        """
        Removes the specified field from the instance or collection.

        This method is used to delete a specific field identified by
        its name. It ensures the designated field is removed entirely
        from the relevant data structure. No value is returned upon
        successful execution.

        Args:
            field_name (str): The name of the field to be removed.

        Returns:
            Any: The value of the removed field, if any.
        """
        return self.fields.pop(field_name, None)

    cpdef int count(self):
        """
        Counts the total number of elements in the collection.

        This method returns the total count of elements stored within the
        underlying data structure, providing a quick way to ascertain the
        size or number of entries available.

        Returns:
            int: The total number of elements in the collection.
        """
        return len(self.fields)

    cpdef void replace(
        self,
        name: str,
        required: bool = False,
        default: Any = None,
        fallback: Any = None,
        filters: Optional[List[BaseFilter]] = None,
        validators: Optional[List[BaseValidator]] = None,
        steps: Optional[List[Union[BaseFilter, BaseValidator]]] = None,
        external_api: Optional[ExternalApiConfig] = None,
        copy: Optional[str] = None,
    ):
        """
        Replaces a field in the input filter.

        Args:
             name (str): The name of the field.
            
            required (Optional[bool]): Whether the field is required.
            
            default (Optional[Any]): The default value of the field.
            
            fallback (Optional[Any]): The fallback value of the field, if 
                validations fails or field None, although it is required.
                
            filters (Optional[List[BaseFilter]]): The filters to apply to 
                the field value.
            
            validators (Optional[List[BaseValidator]]): The validators to 
                apply to the field value.
                
            steps (Optional[List[Union[BaseFilter, BaseValidator]]]): Allows 
                to apply multiple filters and validators in a specific order.
                
            external_api (Optional[ExternalApiConfig]): Configuration for an 
                external API call.
            
            copy (Optional[str]): The name of the field to copy the value 
                from.
        """
        self.fields[name] = FieldModel(
            required=required,
            default=default,
            fallback=fallback,
            filters=filters or [],
            validators=validators or [],
            steps=steps or [],
            external_api=external_api,
            copy=copy,
        )

    cdef object applySteps(
        self,
        steps: List[Union[BaseFilter, BaseValidator]],
        fallback: Any,
        value: Any,
    ):
        """
        Apply multiple filters and validators in a specific order.

        This method processes a given value by sequentially applying a list of 
        filters and validators. Filters modify the value, while validators 
        ensure the value meets specific criteria. If a validation error occurs 
        and a fallback value is provided, the fallback is returned. Otherwise, 
        the validation error is raised.

        Args:
            steps (List[Union[BaseFilter, BaseValidator]]): 
                A list of filters and validators to be applied in order.
            fallback (Any): 
                A fallback value to return if validation fails.
            value (Any): 
                The initial value to be processed.

        Returns:
            Any: The processed value after applying all filters and validators. 
                If a validation error occurs and a fallback is provided, the 
                fallback value is returned.

        Raises:
            ValidationError: If validation fails and no fallback value is 
                provided.
        """
        if value is None:
            return

        try:
            for step in steps:
                if isinstance(step, BaseFilter):
                    value = step.apply(value)
                elif isinstance(step, BaseValidator):
                    step.validate(value)
        except ValidationError:
            if fallback is None:
                raise
            return fallback
        return value

    @staticmethod
    cdef object checkForRequired(
        field_name: str,
        required: bool,
        default: Any,
        fallback: Any,
        value: Any,
    ):
        """
        Determine the value of the field, considering the required and
        fallback attributes.

        If the field is not required and no value is provided, the default
        value is returned. If the field is required and no value is provided,
        the fallback value is returned. If no of the above conditions are met,
        a ValidationError is raised.
        
        Args:
            field_name (str): The name of the field being processed.
            required (bool): Indicates whether the field is required.
            default (Any): The default value to use if the field is not provided and not required.
            fallback (Any): The fallback value to use if the field is required but not provided.
            value (Any): The current value of the field being processed.

        Returns:
            Any: The determined value of the field after considering required, default, and fallback attributes.

        Raises:
            ValidationError: If the field is required and no value or fallback is provided.
        """
        if value is not None:
            return value

        if not required:
            return default

        if fallback is not None:
            return fallback

        raise ValidationError(f"Field '{field_name}' is required.")

    cpdef void addGlobalFilter(self, filter: BaseFilter):
        """
        Add a global filter to be applied to all fields.

        Args:
            filter: The filter to add.
        """
        self.global_filters.append(filter)

    cpdef list getGlobalFilters(self):
        """
        Retrieve all global filters associated with this InputFilter instance.

        This method returns a list of BaseFilter instances that have been
        added as global filters. These filters are applied universally to
        all fields during data processing.

        Returns:
            List[BaseFilter]: A list of global filters.
        """
        return self.global_filters

    cdef object applyFilters(self, filters: List[BaseFilter], value: Any):
        """
        Apply filters to the field value.
        
        Args:
            filters (List[BaseFilter]): A list of filters to apply to the 
                value.
            value (Any): The value to be processed by the filters.
        
        Returns:
            Any: The processed value after applying all filters. 
                If the value is None, None is returned.
        """
        if value is None:
            return

        for filter in filters:
            value = filter.apply(value)

        return value

    cpdef void clear(self):
        """
        Resets all fields of the InputFilter instance to
        their initial empty state.

        This method clears the internal storage of fields,
        conditions, filters, validators, and data, effectively
        resetting the object as if it were newly initialized.
        """
        self.fields.clear()
        self.conditions.clear()
        self.global_filters.clear()
        self.global_validators.clear()
        self.data.clear()
        self.validated_data.clear()
        self.errors.clear()

    cpdef void merge(self, other: InputFilter):
        """
        Merges another InputFilter instance intelligently into the current
        instance.

        - Fields with the same name are merged recursively if possible,
            otherwise overwritten.
        - Conditions, are combined and duplicated.
        - Global filters and validators are merged without duplicates.

        Args:
            other (InputFilter): The InputFilter instance to merge.
        """
        if not isinstance(other, InputFilter):
            raise TypeError(
                "Can only merge with another InputFilter instance."
            )

        for key, new_field in other.getInputs().items():
            self.fields[key] = new_field

        self.conditions += other.conditions

        for filter in other.global_filters:
            existing_type_map = {
                type(v): i for i, v in enumerate(self.global_filters)
            }
            if type(filter) in existing_type_map:
                self.global_filters[existing_type_map[type(filter)]] = filter
            else:
                self.global_filters.append(filter)

        for validator in other.global_validators:
            existing_type_map = {
                type(v): i for i, v in enumerate(self.global_validators)
            }
            if type(validator) in existing_type_map:
                self.global_validators[
                    existing_type_map[type(validator)]
                ] = validator
            else:
                self.global_validators.append(validator)

    cpdef void setModel(self, model_class: Type[T]):
        """
        Set the model class for serialization.

        Args:
            model_class (Type[T]): The class to use for serialization.
        """
        self.model_class = model_class

    cpdef object serialize(self):
        """
        Serialize the validated data. If a model class is set,
        returns an instance of that class, otherwise returns the
        raw validated data.

        Returns:
            Union[Dict[str, Any], T]: The serialized data.
        """
        if self.model_class is None:
            return self.validated_data

        return self.model_class(**self.validated_data)

    cpdef void addGlobalValidator(self, validator: BaseValidator):
        """
        Add a global validator to be applied to all fields.

        Args:
            validator (BaseValidator): The validator to add.
        """
        self.global_validators.append(validator)

    cpdef list getGlobalValidators(self):
        """
        Retrieve all global validators associated with this
        InputFilter instance.

        This method returns a list of BaseValidator instances that have been
        added as global validators. These validators are applied universally
        to all fields during validation.

        Returns:
            List[BaseValidator]: A list of global validators.
        """
        return self.global_validators

    cdef object validateField(
        self, validators: List[BaseValidator], fallback: Any, value: Any
    ):
        """
        Validate the field value.

        Args:
            validators (List[BaseValidator]): A list of validators to apply 
                to the field value.
            fallback (Any): A fallback value to return if validation fails.
            value (Any): The value to be validated.

        Returns:
            Any: The validated value if all validators pass. If validation 
                fails and a fallback is provided, the fallback value is 
                returned.
        """
        if value is None:
            return

        try:
            for validator in validators:
                validator.validate(value)
        except ValidationError:
            if fallback is None:
                raise

            return fallback
