# TTL_Chache_Decorator
A decorator that saves any caculated outputs for every function it wraps in a database wil a TTL
For every call to the function with the same arguments within the TTL the TTL count will reset
once the TTL expires the arguments and output will be delted from the data structure
