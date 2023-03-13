# Manchester Bin Collections

This is a custom component for Home Assistant which integrates with the Manchester City Council website and gets the bin collection information for your address.

A sensor will be created for each bin showing the next date that bin is due to be collected.

Additionally there are three other sensors created:

- A binary sensor which is true if one or more bins are due for collection tomorrow
- A binary sensor which is true if one or more bins are due for collection today
- A sensor with a text value of which bins are due for collection next


## Installation

Copy the `manchester_bins` folder to the `custom_components` folder inside your HA config directory. If a `custom_components` folder does not exist, just create it.

Next restart Home Assistant.

Setting up this component is done entirely in the UI. Go to your Integration settings, press to add a new integration, and find "Manchester Bins".

The setup wizard will first ask you to enter your post code. This must be a post code that falls under Manchester City Council's responsibility.

Next the setup wizard will list all the street addresses found under that post code, select which one is yours.

These steps are necessary, as each address has it's own ID which is needed to get the bin collection information. It is just this ID that is stored, not anything else.

And that is all there is too it! The integration should now be showing on your list, along with a number of new entities for all the sensors it has created.