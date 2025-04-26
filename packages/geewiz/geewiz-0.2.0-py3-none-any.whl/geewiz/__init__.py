from geewiz.client import GeewizClient

# This is for whe you want to use geewiz like:
#
#   from geewiz import geewiz, var
#   geewiz.card(...)
#   var.my_var = "my value"

geewiz = GeewizClient()

# These are for when you want to use geewiz like:
#
#   import geewiz
#   geewiz.card(...)
#   geewiz.var.my_var = "my value"

card = geewiz.card
get_user_config = geewiz.get_user_config
progress = geewiz.progress
resend_last_card = geewiz.resend_last_card
set = geewiz.set
set_input = geewiz.set_input
set_output = geewiz.set_output
var = geewiz.var
variables = geewiz.variables
