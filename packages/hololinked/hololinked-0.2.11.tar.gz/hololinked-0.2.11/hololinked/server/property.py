import typing
from types import FunctionType, MethodType
from enum import Enum


from ..param.parameterized import Parameter, ClassParameters, Parameterized, ParameterizedMetaclass
from .utils import issubklass, pep8_to_URL_path
from .dataklasses import RemoteResourceInfoValidator
from .constants import USE_OBJECT_NAME, HTTP_METHODS
from .events import Event, EventDispatcher
from .schema_validators import JsonSchemaValidator



class Property(Parameter):
    """
    Initialize a new Property object and to get/set/delete an object/instance attribute. Please note the capital 'P' in 
    Property to differentiate from python's own ``property``. ``Property`` objects are similar to python ``property``
    but not a subclass of it due to limitations and redundancy.

    Parameters
    ----------

    default: None or corresponding to property type 
        The default value of the property. 

    doc: str, default empty
        docstring explaining what this property represents.

    constant: bool, default False
        if True, the Property value can be changed only once when ``allow_None`` is set to True. The
        value is otherwise constant on the ``Thing`` instance.

    readonly: bool, default False
        if True, the Property value cannot be changed by setting the attribute at the class or instance
        levels at all. Either the value is fetched always or a getter method is executed which may still generate dynamic
        values at each get/read operation.

    allow_None: bool, default False 
        if True, None is accepted as a valid value for this Property, in addition to any other values that are
        allowed. 

    URL_path: str, uses object name by default
        resource locator under which the attribute is accessible through HTTP. When not given, the variable name 
        is used and underscores are replaced with dash

    http_method: tuple, default ("GET", "PUT", "DELETE")
        http methods for read, write and delete respectively 

    observable: bool, default False
        set to True to receive change events. Supply a function if interested to evaluate on what conditions the change 
        event must be emitted. Default condition is a plain not-equal-to operator.

    state: str | Enum, default None
        state of state machine where property write can be executed

    db_persist: bool, default False
        if True, every write is stored in database and property value persists ``Thing`` instance destruction and creation. 
        The loaded value from database is written into the property at ``Thing.__post_init__``.
        set ``Thing.use_default_db`` to True, to avoid setting up a database or supply a ``db_config_file``.
    
    db_init: bool, default False
        if True, property's first value is loaded from database and written using setter. 
        Further writes are not written to database. if ``db_persist`` is True, this value is ignored. 

    db_commit: bool,
        if True, all write values are stored to database. The database value is not loaded at ``Thing.__post_init__()``. 
        if db_persist is True, this value is ignored. 

    fget: Callable, default None
        custom getter method, mandatory when setter method is also custom supplied.

    fset: Callable, default None
        custom setter method
    
    fdel: Callable, default None
        custom deleter method

    remote: bool, default True
        set to false to make the property local/not remotely accessible

    label: str, default extracted from object name
        optional text label to be used when this Property is shown in a listing. If no label is supplied, 
        the attribute name for this property in the owning ``Thing`` object is used.
    
    metadata: dict, default None
        store your own JSON compatible metadata for the property which gives useful (and modifiable) information 
        about the property. Properties operate using slots which means you cannot set foreign attributes on this object 
        normally. This metadata dictionary should overcome this limitation. 

    per_instance_descriptor: bool, default False 
        whether a separate Property instance will be created for every ``Thing`` instance. True by default.
        If False, all instances of a ```Thing``` class will share the same Property object, including all validation
        attributes (bounds, allow_None etc.). 

    deepcopy_default: bool, default False 
        controls whether the default value of this Property will be deepcopied when a ``Thing`` object is instantiated (if
        True), or if the single default value will be shared by all ``Thing`` instances (if False). For an immutable 
        Property value, it is best to leave deep_copy at the default of False. For a mutable Property value, 
        for example - lists and dictionaries, the default of False is also appropriate if you want all instances to share 
        the same value state, e.g. if they are each simply referring to a single global object like a singleton. 
        If instead each ``Thing`` should have its own independently mutable value, deep_copy should be set to
        True. This setting is similar to using ``field``'s ``default_factory`` in python dataclasses.

    class_member : bool, default False
        when True, property is set on ``Thing`` class instead of ``Thing`` instance. 

    precedence: float, default None
        a numeric value, usually in the range 0.0 to 1.0, which allows the order of Properties in a class to be defined in
        a listing or e.g. in GUI menus. A negative precedence indicates a property that should be hidden in such listings.

    """

    __slots__ = ['db_persist', 'db_init', 'db_commit', 'metadata', 'model', 'validator', '_remote_info', 
                '_observable', '_observable_event_descriptor', 'fcomparator', '_old_value_internal_name']
    
    # RPC only init - no HTTP methods for those who dont like
    @typing.overload
    def __init__(self, default: typing.Any = None, *, doc : typing.Optional[str] = None, constant : bool = False, 
                readonly : bool = False, allow_None : bool = False, observable : bool = False, 
                state : typing.Optional[typing.Union[typing.List, typing.Tuple, str, Enum]] = None,
                db_persist : bool = False, db_init : bool = False, db_commit : bool = False,  remote : bool = True,
                class_member : bool = False, fget : typing.Optional[typing.Callable] = None, 
                fset : typing.Optional[typing.Callable] = None, fdel : typing.Optional[typing.Callable] = None,
            ) -> None:
        ...

    @typing.overload
    def __init__(self, default: typing.Any = None, *, doc : typing.Optional[str] = None, constant : bool = False, 
                readonly : bool = False, allow_None : bool = False, URL_path : str = USE_OBJECT_NAME, 
                http_method : typing.Tuple[typing.Optional[str], typing.Optional[str]] = (HTTP_METHODS.GET, HTTP_METHODS.PUT), 
                observable : bool = False, state : typing.Optional[typing.Union[typing.List, typing.Tuple, str, Enum]] = None,
                db_persist : bool = False, db_init : bool = False, db_commit : bool = False, remote : bool = True, 
                class_member : bool = False, fget : typing.Optional[typing.Callable] = None, 
                fset : typing.Optional[typing.Callable] = None, fdel : typing.Optional[typing.Callable] = None, 
                metadata : typing.Optional[typing.Dict] = None
            ) -> None:
        ...

    @typing.overload
    def __init__(self, default: typing.Any = None, *, doc : typing.Optional[str] = None, constant : bool = False, 
                readonly : bool = False, allow_None : bool = False, 
                URL_path : str = USE_OBJECT_NAME, 
                http_method : typing.Tuple[typing.Optional[str], typing.Optional[str], typing.Optional[str]] = 
                                                            (HTTP_METHODS.GET, HTTP_METHODS.PUT, HTTP_METHODS.DELETE), 
                observable : bool = False, change_comparator : typing.Optional[typing.Union[FunctionType, MethodType]] = None,
                state : typing.Optional[typing.Union[typing.List, typing.Tuple, str, Enum]] = None,
                db_persist : bool = False, db_init : bool = False, db_commit : bool = False, remote : bool = True,
                class_member : bool = False, fget : typing.Optional[typing.Callable] = None, 
                fset : typing.Optional[typing.Callable] = None, fdel : typing.Optional[typing.Callable] = None, 
                fcomparator : typing.Optional[typing.Callable] = None, 
                deepcopy_default : bool = False, per_instance_descriptor : bool = False, 
                precedence : typing.Optional[float] = None, metadata : typing.Optional[typing.Dict] = None
            ) -> None:
        ...
 
    def __init__(self, default: typing.Any = None, *, 
                doc : typing.Optional[str] = None, constant : bool = False, 
                readonly : bool = False, allow_None : bool = False, label : typing.Optional[str] = None, 
                URL_path : str = USE_OBJECT_NAME, 
                http_method : typing.Tuple[typing.Optional[str], typing.Optional[str], typing.Optional[str]] = 
                                                            (HTTP_METHODS.GET, HTTP_METHODS.PUT, HTTP_METHODS.DELETE), 
                state : typing.Optional[typing.Union[typing.List, typing.Tuple, str, Enum]] = None,
                db_persist : bool = False, db_init : bool = False, db_commit : bool = False, 
                observable : bool = False, class_member : bool = False, model = None, 
                fget : typing.Optional[typing.Callable] = None, fset : typing.Optional[typing.Callable] = None, 
                fdel : typing.Optional[typing.Callable] = None, fcomparator : typing.Optional[typing.Callable] = None,  
                deepcopy_default : bool = False, per_instance_descriptor : bool = False, remote : bool = True, 
                precedence : typing.Optional[float] = None, metadata : typing.Optional[typing.Dict] = None
            ) -> None:
        super().__init__(default=default, doc=doc, constant=constant, readonly=readonly, allow_None=allow_None,
                    label=label, per_instance_descriptor=per_instance_descriptor, deepcopy_default=deepcopy_default,
                    class_member=class_member, fget=fget, fset=fset, fdel=fdel, precedence=precedence)
        self.db_persist = db_persist
        self.db_init    = db_init
        self.db_commit  = db_commit
        self.fcomparator = fcomparator
        self.metadata = metadata
        self._observable = observable
        self._observable_event_descriptor : Event = None
        self._remote_info = None
        if remote:
            self._remote_info = RemoteResourceInfoValidator(
                http_method=http_method,
                URL_path=URL_path,
                state=state,
                isproperty=True
            )
        self.model = None
        self.validator = None
        if model:
            if isinstance(model, dict):
                self.model = model
                self.validator = JsonSchemaValidator(model)
            else:
                self.model = wrap_plain_types_in_rootmodel(model) # type: BaseModel
                self.validator = self.model.model_validate
               

    def __set_name__(self, owner: typing.Any, attrib_name: str) -> None:
        super().__set_name__(owner, attrib_name)
        self._old_value_internal_name = f'{self._internal_name}_old_value'
        if self._remote_info is not None:
            if self._remote_info.URL_path == USE_OBJECT_NAME:
                self._remote_info.URL_path = f'/{pep8_to_URL_path(self.name)}'
            elif not self._remote_info.URL_path.startswith('/'): 
                raise ValueError(f"URL_path should start with '/', please add '/' before '{self._remote_info.URL_path}'")
            self._remote_info.obj_name = self.name
        if self._observable:
            _observable_event_name = f'{self.name}_change_event'  
            # This is a descriptor object, so we need to set it on the owner class
            self._observable_event_descriptor = Event(
                        friendly_name=_observable_event_name,
                        URL_path=f'{self._remote_info.URL_path}/change-event',
                        doc=f"change event for {self.name}"
                    ) # type: Event
            self._observable_event_descriptor.__set_name__(owner, _observable_event_name)
            setattr(owner, _observable_event_name, self._observable_event_descriptor)
    

    def __get__(self, obj: Parameterized, objtype: ParameterizedMetaclass) -> typing.Any:
        read_value = super().__get__(obj, objtype)
        self._push_change_event_if_needed(obj, read_value)
        return read_value
      

    def _push_change_event_if_needed(self, obj, value : typing.Any) -> None:
        """
        Pushes change event both on read and write if an event publisher object is available
        on the owning Thing.        
        """
        if self._observable and obj.event_publisher:
            event_dispatcher = getattr(obj, self._observable_event_descriptor._obj_name, None) # type: EventDispatcher
            old_value = obj.__dict__.get(self._old_value_internal_name, NotImplemented)
            obj.__dict__[self._old_value_internal_name] = value 
            if self.fcomparator:
                if issubklass(self.fcomparator):
                    if not self.fcomparator(self.owner, old_value, value):
                        return 
                elif not self.fcomparator(obj, old_value, value):
                    return
            elif not old_value != value:
                return 
            event_dispatcher.push(value)       


    def validate_and_adapt(self, value) -> typing.Any:
        if value is None:
            if self.allow_None:
                return value 
            else:
                raise ValueError(f"Property {self.name} does not allow None values")
        if self.model:
            if isinstance(self.model, dict):
                self.validator.validate(value)
            elif issubklass(self.model, BaseModel):
                self.validator(value)
        return super().validate_and_adapt(value)
    

    def _post_value_set(self, obj, value : typing.Any) -> None:
        if (self.db_persist or self.db_commit) and hasattr(obj, 'db_engine'):
            from .thing import Thing
            assert isinstance(obj, Thing), f"database property {self.name} bound to a non Thing, currently not supported"
            obj.db_engine.set_property(self, value)
        self._push_change_event_if_needed(obj, value)
        return super()._post_value_set(obj, value)
    
    
    def comparator(self, func : typing.Callable) -> typing.Callable:
        """
        Register a comparator method by using this as a decorator to decide when to push
        a change event.
        """
        self.fcomparator = func 
        return func
    

    
__property_info__ = [
                'allow_None' , 'class_member', 'db_init', 'db_persist', 
                'db_commit', 'deepcopy_default', 'per_instance_descriptor', 
                'state', 'precedence', 'constant', 'default'
                # 'scada_info', 'property_type' # descriptor related info is also necessary
            ]

   
class ClassProperties(ClassParameters):
    """
    Object that holds the namespace and implementation of Parameterized methods as well as any state that is not 
    in __slots__ or the Properties themselves.
    Exists at metaclass level (instantiated by the metaclass). Contains state specific to the class.
    """

    @property
    def db_persisting_objects(self):
        try:
            return getattr(self.owner_cls, f'_{self.owner_cls.__name__}_db_persisting_remote_params')
        except AttributeError: 
            paramdict = self.remote_objects
            db_persisting_remote_params = {}
            for name, desc in paramdict.items():
                if desc.db_persist:
                    db_persisting_remote_params[name] = desc
            setattr(self.owner_cls, f'_{self.owner_cls.__name__}_db_persisting_remote_params', db_persisting_remote_params)
        return getattr(self.owner_cls, f'_{self.owner_cls.__name__}_db_persisting_remote_params')

    @property
    def db_init_objects(self) -> typing.Dict[str, Property]:
        try:
            return getattr(self.owner_cls, f'_{self.owner_cls.__name__}_db_init_remote_params')
        except AttributeError: 
            paramdict = self.remote_objects
            init_load_params = {}
            for name, desc in paramdict.items():
                if desc.db_init or desc.db_persist:
                    init_load_params[name] = desc
            setattr(self.owner_cls, f'_{self.owner_cls.__name__}_db_init_remote_params', init_load_params)
        return getattr(self.owner_cls, f'_{self.owner_cls.__name__}_db_init_remote_params')
        
    @property
    def remote_objects(self) -> typing.Dict[str, Property]:
        try:
            return getattr(self.owner_cls, f'_{self.owner_cls.__name__}_remote_params')
        except AttributeError: 
            paramdict = super().descriptors
            remote_params = {}
            for name, desc in paramdict.items():
                if isinstance(desc, Property):
                    remote_params[name] = desc
            setattr(self.owner_cls, f'_{self.owner_cls.__name__}_remote_params', remote_params)
        return getattr(self.owner_cls, f'_{self.owner_cls.__name__}_remote_params')

    def webgui_info(self, for_remote_params : typing.Union[Property, typing.Dict[str, Property], None] = None):
        info = {}
        if isinstance(for_remote_params, dict):
            objects = for_remote_params 
        elif isinstance(for_remote_params, Property):
            objects = { for_remote_params.name : for_remote_params } 
        else:
            objects = self.remote_objects
        for param in objects.values():
            state = param.__getstate__()
            info[param.name] = dict(
                python_type = param.__class__.__name__,
            )
            for field in __property_info__:
                info[param.name][field] = state.get(field, None) 
        return info 

    
try: 
    from pydantic import BaseModel, RootModel, create_model
    def wrap_plain_types_in_rootmodel(model : type) -> type["BaseModel"]:
        """
        Ensure a type is a subclass of BaseModel.

        If a `BaseModel` subclass is passed to this function, we will pass it
        through unchanged. Otherwise, we wrap the type in a RootModel.
        In the future, we may explicitly check that the argument is a type
        and not a model instance.
        """
        try:  # This needs to be a `try` as basic types are not classes
            assert issubclass(model, BaseModel)
            return model
        except (TypeError, AssertionError):
            return create_model(f"{model!r}", root=(model, ...), __base__=RootModel)
        except NameError:
            raise ImportError("pydantic is not installed, please install it to use this feature") from None
except ImportError:
    def wrap_plain_types_in_rootmodel(model : type) -> type:
        raise ImportError("pydantic is not installed, please install it to use this feature") from None
  

__all__ = [
    Property.__name__
]