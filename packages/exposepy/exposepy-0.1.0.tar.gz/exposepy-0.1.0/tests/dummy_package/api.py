from dummy_package.core import original_func
from expose import reexpose

# Reexpose with alias in API layer
reexpose(original_func, name="public_func")

