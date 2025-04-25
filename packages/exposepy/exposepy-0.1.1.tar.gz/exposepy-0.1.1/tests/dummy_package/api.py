from dummy_package.core import original_func
from exposepy import reexpose

# Reexpose with alias in API layer
reexpose(original_func, name="public_func")

