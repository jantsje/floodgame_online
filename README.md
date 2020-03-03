# floodgame_online

This application allows to use the Floodgame as an oTree application in Dutch with five treatments. The experiment was conducted in July 2018 among 2111 homeowners in the Dutch river delta.

## Published paper
Mol, J. M., Botzen, W. J. W., & Blasch, J. E. (2018). Behavioral motivations for self-insurance under different disaster risk insurance schemes. Journal of Economic Behavior & Organization, 1–25. https://doi.org/10.1016/j.jebo.2018.12.007

## Installation
To install the app to your local oTree directory, copy the folder 'floodgame_online' to your oTree Django project and extent the session configurations in your settings.py at the root of the oTree directory:

```
SESSION_CONFIGS = [
    dict(
        name='floodgame_online',
        display_name="Floodgame online",
        num_demo_participants=1,
        app_sequence=['floodgame_online'],
        quota_discount=1,
        quota_baseline=1,
        quota_voluntary=1,
        quota_voluntary_discount=1,
        quota_no_insurance=1,
        language='nl'
    )
```

Understanding questions rely on [otree-utils](https://github.com/WZBSocialScienceCenter/otreeutils) and are different for each treatment.

## Treatments
* no insurance (mandatory no insurance)
* baseline (mandatory insurance)
* discount (mandatory insurance, discount offered on premium when pp invested in damage-reducing measures)
* voluntary (includes WTP pages, pp with WTP > subsidized premium are insured in the game)
* voluntary discount (includes WTP pages, pp with WTP > subsidized premium are insured in the game, discount offered)

## Target group
Note that the first page ('Welkom') asks for homeownership and postal code. The 'postcodes.py' file is used as input to determine whether a respondent is in the target area. 
Respondents who answer that they do not own their home or those who enter a postcode that is not in 'postcodes.py' will be redirected to the no-target-group-message of the panel company. 

## Instructions pop-up
Instructions are available in a pop-up screen (modal) throughout the game. JavaScript code tracks how often respondents click this button ('opened_instructions').
