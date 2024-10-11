from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from floodgame_online import vragen, postcodes_1_1250
import random  # necessary for random risk_high


author = 'Jantsje Mol'

doc = """
Investeringsfloodgame_online voor huiseigenaren (online versie in het Nederlands)
"""


class Constants(BaseConstants):
    name_in_url = 'spel'
    players_per_group = None
    scenarios = ["LH"]
    scenarios_no_insurance = ["risk1"]
    num_start_pages = 5
    num_end_pages = 8
    num_test_years = 1
    num_def_years = 1
    num_rounds = num_start_pages + num_test_years + num_def_years + num_end_pages
    risk = 1
    deductible = float(0.05)
    damage = c(50000)  # size of damage in case of a flood
    lower_premium = 0.8
    jaar = 25
    scaling_lossfunction = -0.0002
    house_value = c(240000)
    initial_endowment = c(65000)
    total_earnings = house_value + initial_endowment
    willingness_values = list(range(0, 11))
    fair = c(40)
    monthly_subsidized = c(32)

    ''' houses for floodrisk  '''
    itemss = list(range(1, 51))
    items = ["{0:0=3d}".format(value) for value in itemss]
    itemss2 = list(range(51, 101))
    items2 = ["{0:0=3d}".format(value) for value in itemss2]


class Subsession(BaseSubsession):

    def creating_session(self):
        if self.round_number == 1:

            self.session.vars["mitigation_cost"] = [0, 1000, 5000, 10000, 15000]
            #                               name treatment        niet doelgroep, doelgroep, completed
            self.session.vars["telling"] = {"no insurance":         ([], [], []),
                                            "baseline":             ([], [], []),
                                            "discount":             ([], [], []),
                                            "voluntary":            ([], [], []),
                                            "voluntary discount":   ([], [], []),
                                            "not yet":              ([], [], [])
                                            }

        for p in self.get_players():

            sconfig = self.session.config

            self.session.vars["combinations"] = []  # has_insurance, has_discount, is_voluntary, name of treatment
            if self.session.config['quota_discount'] > 0:
                self.session.vars["combinations"].append([[True, True, False, "discount"]])
            if self.session.config['quota_baseline'] > 0:
                self.session.vars["combinations"].append([[True, False, False, "baseline"]])
            if self.session.config['quota_no_insurance'] > 0:
                self.session.vars["combinations"].append([[False, False, False, "no insurance"]])
            if self.session.config['quota_voluntary'] > 0:
                self.session.vars["combinations"].append([[False, False, True, "voluntary"]])
            if self.session.config['quota_voluntary_discount'] > 0:
                self.session.vars["combinations"].append([[False, True, True, "voluntary discount"]])

            if 'has_insurance' in sconfig:
                p.participant.vars["has_insurance"] = sconfig.get('has_insurance')
                p.has_discount = sconfig.get('has_discount')
                p.is_voluntary = sconfig.get('is_voluntary')
                p.participant.vars["treatment"] = sconfig.get('treatment')
            else:
                p.participant.vars["has_insurance"] = 'not yet'
                p.participant.vars["has_discount"] = 'not yet'
                p.participant.vars["is_voluntary"] = 'not yet'
                p.participant.vars["treatment"] = 'not yet'  # you need something here to be able to append

            if self.round_number == 1:
                p.participant.vars["flooded"] = False
                self.session.vars["quotafull"] = False
                p.participant.vars["doelgroep"] = 'not answered yet'
                p.participant.vars["conversion"] = sconfig.get('real_world_currency_per_point')
                p.participant.vars["max_payoff"] = 0
                p.participant.vars["wtp"] = ''
                p.participant.vars["timespent"] = ''
                p.participant.vars["insurance_choice"] = False
                p.participant.vars["edu_text_needed"] = False
                p.participant.vars["page_title"] = ''
                p.participant.vars["difficult_text_needed"] = False
                p.participant.vars["evacuated_text_needed"] = False
                p.participant.vars["neighbors_needed"] = False
                p.participant.vars["opened_instructions"] = 0
                p.participant.vars["selected_scenario"] = random.randint(1, 6)
                p.participant.vars["selected_pref"] = random.randint(1, 7)
                p.participant.vars["selected_additional"] = random.randint(1, 3)
                p.participant.vars["payoff_small"] = 0
                p.participant.vars["left_selected"] = random.choice([True, False])
                p.participant.vars["left_selected2"] = random.choice([True, False])
                p.participant.vars["cumulative_payoff"] = 0
                p.participant.vars["mitigate_more"] = 0
                p.participant.vars["payoff_scenario1"] = 0
                p.participant.vars["page_title"] = ""
                p.participant.vars["premium"] = 999999  # set initial value
                p.participant.vars["total_premium"] = 99999
                p.participant.vars["premium_discounted"] = [c(32)*12, c(335), c(193), c(80), c(11)]
                p.participant.vars["reduced_deductible"] = [c(0), c(0), c(0), c(0), c(0)]
                p.participant.vars["reduced_damage"] = (c(50000), c(45242), c(30327), c(18394), c(11157))
                p.participant.vars["mitigation_cost"] = ([c(0), c(1000), c(5000), c(10000), c(15000)])
                p.participant.vars["mitigated_before"] = 0
                p.participant.vars["in_scenario"] = False
                p.participant.vars["mitigated_this_scenario"] = 999
                p.participant.vars["mitigation_cost_this_scenario"] = 999
                p.participant.vars["deductible_ecu_this_scenario"] = 999
                p.participant.vars["deductible_percent"] = 999
                p.participant.vars["floodrisk_percent"] = 999
                p.participant.vars["reduced_damage_this_scenario"] = Constants.damage
                p.mitigation_cost = 0  # fixme why not 999?

                # if p.participant.vars["has_insurance"]:
                #     p.participant.vars["scenarios"] = Constants.scenarios.copy()
                # else:
                #     p.participant.vars["scenarios"] = Constants.scenarios_no_insurance.copy()

            if self.round_number == 6 or self.round_number == 7:

                flood_nrs = []
                for year in range(1, Constants.jaar + 1):
                    flood_nr = random.sample(range(1, 101), Constants.risk)
                    flood_nrs.append(*flood_nr)
                flood_nrs_unique = list(set(flood_nrs))
                p.floodnrs = str(["{0:0=3d}".format(value) for value in flood_nrs_unique])
                if "012" in p.floodnrs:
                    p.flooded = True
                else:
                    p.flooded = False

            p.high_risk = False
            p.deductible = Constants.deductible
            p.risk = Constants.risk
            p.level_deductible = 1

    def vars_for_admin_report(self):
        doelgroep = [len(self.session.vars["telling"]["no insurance"][0]) +
                     len(self.session.vars["telling"]["baseline"][0]) +
                     len(self.session.vars["telling"]["discount"][0]) +
                     len(self.session.vars["telling"]["voluntary"][0]) +
                     len(self.session.vars["telling"]["voluntary discount"][0])]
        dropouts = [len(self.session.vars["telling"]["no insurance"][1]) -
                    len(self.session.vars["telling"]["no insurance"][2]),
                    len(self.session.vars["telling"]["baseline"][1]) -
                    len(self.session.vars["telling"]["baseline"][2]),
                    len(self.session.vars["telling"]["discount"][1]) -
                    len(self.session.vars["telling"]["discount"][2]),
                    len(self.session.vars["telling"]["voluntary"][1]) -
                    len(self.session.vars["telling"]["voluntary"][2]),
                    len(self.session.vars["telling"]["voluntary discount"][1]) -
                    len(self.session.vars["telling"]["voluntary discount"][2]),
                    len(self.session.vars["telling"]["not yet"][1])]
        completes = [len(self.session.vars["telling"]["no insurance"][2]),
                     len(self.session.vars["telling"]["baseline"][2]),
                     len(self.session.vars["telling"]["discount"][2]),
                     len(self.session.vars["telling"]["voluntary"][2]),
                     len(self.session.vars["telling"]["voluntary discount"][2])]
        quota = [self.session.config['quota_no_insurance'],
                 self.session.config['quota_baseline'],
                 self.session.config['quota_discount'],
                 self.session.config['quota_voluntary'],
                 self.session.config['quota_voluntary_discount']]
        vars_admin_list = [[p.participant.code,
                            p.participant.vars["treatment"],
                            p.participant.vars["wtp"],
                            p.participant.vars["mitigation_cost_this_scenario"],
                            p.participant.vars["timespent"]]
                           for p in self.get_players()]
        return {'vars_admin_list': vars_admin_list,  'doelgroep': doelgroep,
                'dropouts': dropouts, 'dropouts_totaal': sum(dropouts),
                'completes_totaal': sum(completes), 'completes.txt': completes,
                'quota': quota, 'quota_totaal': sum(quota)}


class Group(BaseGroup):  # it is an individual decision making game
    pass


class Player(BasePlayer):

    # you first need to set up fields for the variables,
    # they are later changed in the set_payoffs and before_session_starts methods

    # has_insurance = models.BooleanField()
    browser = models.StringField()
    store_has_discount = models.BooleanField()
    store_is_voluntary = models.BooleanField()
    store_has_insurance = models.BooleanField()
    store_treatment = models.StringField()
    high_risk = models.BooleanField()
    level_deductible = models.IntegerField()

    understanding_questions_wrong_attempts = models.PositiveIntegerField()
    # number of wrong attempts on understanding questions page
    wtp = models.CurrencyField(min=0, max=Constants.initial_endowment)

    pay_premium = models.StringField()
    mitigate = models.IntegerField(initial=0)  # is necessary for numpy to have an initial value
    koopwoning = models.BooleanField()
    accept_fair = models.BooleanField()
    accept_lower = models.BooleanField()
    mitigation_cost = models.CurrencyField()
    pay_deductible = models.StringField()
    pay_damage = models.StringField()
    floodnr = models.IntegerField()
    flooded = models.BooleanField()
    buy_house = models.StringField()
    scenario = models.StringField()
    scenario_nr = models.IntegerField()
    year = models.IntegerField()
    opened = models.IntegerField(initial=0)
    total_opened = models.IntegerField()

    risk = models.IntegerField()
    deductible = models.FloatField()  # because it has decimals

    premium = models.CurrencyField()
    floodnrs = models.StringField()

    selected = models.StringField()
    selected2 = models.StringField()
    selected_button = models.StringField()
    bigprize = models.StringField()

    # SAVING PAYOFFS FOR RESULTS #######
    payoff_scenario1 = models.CurrencyField()
    total_payoff = models.FloatField()

    ''' vragen importeren voor vragenlijst '''
    ''' Start vragen '''

    # round 1
    age = vragen.age
    gender = vragen.gender
    edu = vragen.edu
    cloud = vragen.cloud
    cloud2 = vragen.cloud2
    # round 2
    flood_prone = vragen.flood_prone
    evacuated = vragen.evacuated
    damaged = vragen.damaged
    flood_prob = vragen.flood_prob
    waterdiepte = vragen.waterdiepte
    # round 3
    evacuated_imagine = vragen.evacuated_imagine
    climate_change = vragen.climate_change
    availability = vragen.availability
    exact_flood_risk_perception = vragen.exact_flood_risk_perception
    expected_damage = vragen.expected_damage
    regret_before = vragen.regret_before
    # round 4
    income = vragen.income
    home = vragen.home
    postcode = vragen.postcode
    postcode_letters = vragen.postcode_letters
    postcode_cijfers = vragen.postcode_cijfers
    floor = vragen.floor
    # round 5
    insurances = vragen.insurances
    insurance = vragen.insurance

    ''' Einde vragen '''
    # round 7
    measures = vragen.measures
    anders_text = vragen.anders_text
    neighbors = vragen.neighbors
    # round 8 if applicable
    neighbors_measures = vragen.neighbors_measures
    # round 8
    perceived_efficacy = vragen.perceived_efficacy
    perceived_cost = vragen.perceived_cost
    self_efficacy = vragen.self_efficacy
    risk_qual = vragen.risk_qual
    risk_qual_spec = vragen.risk_qual_spec
    time_qual = vragen.time_qual
    # round 9
    worry = vragen.worry
    trust = vragen.trust
    concern = vragen.concern
    regret1 = vragen.regret1  # óf
    regret2 = vragen.regret2
    # round 10
    control = vragen.control
    norm1 = vragen.norm1
    norm2 = vragen.norm2

    # round 11
    difficult = vragen.difficult
    explain_strategy = vragen.explain_strategy
    # round 12
    # final round
    difficult_text = vragen.difficult_text
    feedback = vragen.feedback

    sleep = vragen.sleep
    trust2 = vragen.trust2
    no_info = vragen.no_info
    government = vragen.government
    trust_insurer = vragen.trust_insurer
    trust_insurer2 = vragen.trust_insurer2
    control2 = vragen.control2
    control3 = vragen.control3
    control4 = vragen.control4

    def set_treatment(self):
        if self.round_number == 1:
            if not self.session.vars["combinations"]:  # empty list returns False
                self.participant.vars["quotafull"] = True
            else:
                self.participant.vars["quotafull"] = False
                self.participant.vars["combination"] = random.choice(self.session.vars["combinations"])
                self.participant.vars["combination"] = self.participant.vars["combination"][0]
                self.participant.vars["has_insurance"] = self.participant.vars["combination"][0]
                self.participant.vars["has_discount"] = self.participant.vars["combination"][1]
                self.participant.vars["is_voluntary"] = self.participant.vars["combination"][2]
                self.participant.vars["treatment"] = self.participant.vars["combination"][3]
                # now store these in player class to save them to database
                self.store_has_discount = self.participant.vars["has_discount"]
                self.store_is_voluntary = self.participant.vars["is_voluntary"]
                self.store_has_insurance = self.participant.vars["has_insurance"]
                self.store_treatment = self.participant.vars["treatment"]

    def participant_started(self):
        if self.round_number == 1:
            self.session.vars["telling"][self.participant.vars["treatment"]][1].append(self.id_in_group)


    def store_koopwoning(self):
        zipcodes = postcodes_1_1250.zipcodes
        zipcodes = set(zipcodes)
        if not self.koopwoning:
            self.session.vars["telling"][self.participant.vars["treatment"]][0].append(self.id_in_group)
            self.participant.vars["doelgroep"] = False
            # return HttpResponse("WOOW")
        elif self.postcode_cijfers in zipcodes:
            self.session.vars["telling"][self.participant.vars["treatment"]][1].append(self.id_in_group)
            self.participant.vars["doelgroep"] = True
        else:
            self.session.vars["telling"][self.participant.vars["treatment"]][0].append(self.id_in_group)
            self.participant.vars["doelgroep"] = False
        self.session.vars["telling"]["not yet"][1].remove(self.id_in_group)

    def store_complete(self):
        self.session.vars["telling"][self.participant.vars["treatment"]][2].append(self.id_in_group)
        if self.participant.vars["treatment"] == "discount" and \
                len(self.session.vars["telling"]["discount"][2]) == \
                self.session.config['quota_no_insurance']:
            self.session.vars["combinations"].remove([[True, True, False, "discount"]])
        elif self.participant.vars["treatment"] == "baseline" and \
                len(self.session.vars["telling"]["baseline"][2]) == \
                self.session.config['quota_baseline']:
            self.session.vars["combinations"].remove([[True, False, False, "baseline"]])
        elif self.participant.vars["treatment"] == "no insurance" and \
                len(self.session.vars["telling"]["no insurance"][2])\
                == self.session.config['quota_discount']:
            self.session.vars["combinations"].remove([[False, False, False, "no insurance"]])
        elif self.participant.vars["treatment"] == "voluntary" and \
                len(self.session.vars["telling"]["voluntary"][2]) == \
                self.session.config['quota_voluntary']:
            self.session.vars["combinations"].remove([[False, False, True, "voluntary"]])
        elif self.participant.vars["treatment"] == "voluntary discount" and \
                len(self.session.vars["telling"]["voluntary discount"][2]) \
                == self.session.config['quota_voluntary_discount']:
            self.session.vars["combinations"].remove([[False, True, True, "voluntary discount"]])


    def store_follow_up(self):
        if self.difficult == "Moeilijk" or self.difficult == "Heel moeilijk":
            self.participant.vars["difficult_text_needed"] = True  # page 12
        if self.evacuated == "Ja":
            self.participant.vars["evacuated_text_needed"] = True  # page 2
        if self.neighbors == "Ja":
            self.participant.vars["neighbors_needed"] = True  # page 7

    def get_questions_method(self):
        questions = [
            {
                'question': 'Wat was de overstromingskans in het oefenscenario?',
                'options': [str(Constants.risk) + " procent per jaar",
                            "2 procent per jaar",
                            "3 procent per jaar",
                            "4 procent per jaar",
                            "5 procent per jaar",
                            "10 procent per jaar"],
                'correct': str(self.risk) + " procent per jaar",
                'hint': "Het is het aantal huizen dat ieder jaar overstroomde, zie instructies"
            },


        ]

        if self.participant.vars["has_insurance"]:
            questions.append(
                {
                    'question': 'Wat was uw eigen risico in het oefenscenario?',
                    'options': ["5 procent",
                                "10 procent",
                                "15 procent",
                                '50 percent'],
                    'correct': str(self.participant.vars["deductible_percent"]) + " procent",
                    'hint':
                    "Het is het deel van de schade dat u in het geval van een "
                    "overstroming zelf moet betalen, zie het taartdiagram in de instructies"

                },
            )
            if self.participant.vars["has_discount"]:
                questions.append(
                    {
                        'question': 'Wat is het voordeel van schadebeperkende maatregelen?',
                        'options': ["Verminderde schade in het geval van een overstroming",
                                    "Een lagere premie",
                                    "Zowel minder schade als een lagere premie",
                                    "Geen van alle"],
                        'correct': "Zowel minder schade als een lagere premie",
                        'hint': "Lees de instructies nog eens nauwkeurig door."

                    },
                )
            else:
                questions.append(
                    {
                        'question': 'Wat is het voordeel van schadebeperkende maatregelen?',
                        'options': ["Verminderde schade in het geval van een overstroming",
                                    "Een lagere premie",
                                    "Zowel minder schade als een lagere premie",
                                    "Geen van alle"],
                        'correct': "Verminderde schade in het geval van een overstroming",
                        'hint': "Lees de instructies nog eens nauwkeurig door."

                    },
                )
        else:
            questions.append(
                {
                    'question': 'Wat gebeurt er als uw huis overstroomt en '
                                'u heeft niet geïnvesteerd in schadebeperkende maatregelen?',
                    'options': ['Ik zal de volledige schade moeten betalen: ' + str(Constants.damage),
                                'Ik moet een kleine boete betalen',
                                'De overheid zal mij tegemoetkomen in de schade'],
                    'correct': 'Ik zal de volledige schade moeten betalen: ' + str(Constants.damage),
                    'hint': "Lees de instructies nog eens nauwkeurig door."

                },
            )

        return questions

    def vars_for_instructions(self):
        deductible_percent = '{0:.0f}'.format(self.deductible*100)
        return{'deductible_percent': deductible_percent}

    def vars_for_scenarios(self):
        participant = self.participant
        return_vars = {'opened': self.opened,
                       'mitigate': self.mitigate, 'mitigated_before': participant.vars["mitigated_before"],
                       'mitigated_this_scenario': participant.vars["mitigated_this_scenario"],
                       'premium': participant.vars['premium'], 'premium_fair': Constants.fair,
                       'premium_monthly': Constants.monthly_subsidized,
                       'has_insurance': participant.vars["has_insurance"],
                       'deductible': self.deductible,
                       'deductible_ecu_this_scenario': participant.vars["deductible_ecu_this_scenario"],
                       'deductible_percent': participant.vars["deductible_percent"],
                       'premium_discounted': participant.vars["premium_discounted"],
                       'opened_total': self.participant.vars["opened_instructions"],
                       'reduced_damage_this_scenario': participant.vars["reduced_damage_this_scenario"],
                       'koopwoning': self.koopwoning, 'wtp': self.wtp
                       }
        if self.scenario_nr == '0' or self.scenario_nr == 0:
            scenario_type = 'oefenscenario'
            return_vars.update({'scenario_type': scenario_type})
        elif self.scenario_nr == '1' or self.scenario_nr == 1:
            scenario_type = "definitief scenario"
            return_vars.update({'scenario_type': scenario_type})
        else:
            return_vars.update({'scenario_type': ''})
        return return_vars

    def vars_for_invest(self):
        participant = self.participant
        return {'treatment': participant.vars["treatment"],
                'mitigation_cost0': participant.vars["mitigation_cost"][0],
                'mitigation_cost1': participant.vars["mitigation_cost"][1],
                'mitigation_cost2': participant.vars["mitigation_cost"][2],
                'mitigation_cost3': participant.vars["mitigation_cost"][3],
                'mitigation_cost4': participant.vars["mitigation_cost"][4],
                'premium_discounted0': participant.vars["premium_discounted"][0],
                'premium_discounted1': participant.vars["premium_discounted"][1],
                'premium_discounted2': participant.vars["premium_discounted"][2],
                'premium_discounted3': participant.vars["premium_discounted"][3],
                'premium_discounted4': participant.vars["premium_discounted"][4],
                'reduced_deductible0': participant.vars["reduced_deductible"][0],
                'reduced_deductible1': participant.vars["reduced_deductible"][1],
                'reduced_deductible2': participant.vars["reduced_deductible"][2],
                'reduced_deductible3': participant.vars["reduced_deductible"][3],
                'reduced_deductible4': participant.vars["reduced_deductible"][4],
                'mitigation_cost_this_scenario': participant.vars["mitigation_cost_this_scenario"],
                'reduced_damage0': participant.vars["reduced_damage"][0],
                'reduced_damage1': participant.vars["reduced_damage"][1],
                'reduced_damage2': participant.vars["reduced_damage"][2],
                'reduced_damage3': participant.vars["reduced_damage"][3],
                'reduced_damage4': participant.vars["reduced_damage"][4],
                'reduced_damage_this_scenario': participant.vars["reduced_damage_this_scenario"],
                }

    def vars_for_payment(self):
        participant = self.participant
        payoff1 = max(c(participant.vars["payoff_scenario1"]).to_real_world_currency(self.session),
                      c(0).to_real_world_currency(self.session))
        payoff_small_1 = payoff1*0.01

        return {'payoff_small': payoff_small_1, 'payoff': payoff1,
                'payoff_scenario1': participant.vars["payoff_scenario1"],
                'participation_fee': self.session.config['participation_fee'],
                'selected': self.selected,
                }

    def vars_for_payment_prize(self):
        participant = self.participant
        # max to make sure participants do not get a negative payment
        payoff1 = max(c(participant.vars["payoff_scenario1"]).to_real_world_currency(self.session),
                      c(0).to_real_world_currency(self.session))
        payoff_if_selected = payoff1
        self.bigprize = payoff_if_selected
        self.total_payoff = participant.vars["payoff_small"] \
            + self.session.config["participation_fee"] + participant.vars["payoff_additional"]
        payoff_small = participant.vars["payoff_small"]

        return {'participation_fee': self.session.config['participation_fee'],
                'selected_pref': self.participant.vars["selected_pref"],
                'payoff1': str(payoff1) + " now",
                'payoff_small': payoff_small,
                'selected_button': self.selected_button,
                'total_payoff': self.total_payoff,
                'payoff_if_selected': payoff_if_selected,
                'bigprize': self.bigprize,
                }

    def opened_instructions(self):
        self.participant.vars["opened_instructions"] += self.opened

    def pay_premium_method(self):
        if self.pay_premium == "paid_premium":
            self.participant.vars["cumulative_payoff"] -= self.participant.vars["total_premium"]

    def set_insurance(self):
        self.participant.vars["insurance_choice"] = True
        if not self.accept_fair:
            self.participant.vars["has_insurance"] = False
            if not self.accept_lower:
                self.participant.vars["has_insurance"] = False
            elif self.accept_lower:
                self.participant.vars["has_insurance"] = True
        elif self.accept_fair:
            self.participant.vars["has_insurance"] = True

    def pay_after_flood(self):
        if self.pay_damage == "paid_damage":
            self.participant.vars["cumulative_payoff"] -= self.participant.vars["reduced_damage_this_scenario"]
        elif self.pay_deductible == "paid_deductible":
            self.participant.vars["cumulative_payoff"] -= self.participant.vars["deductible_ecu_this_scenario"]

    def pay_mitigation_method(self):
        if 0 < self.mitigate < 999:
            self.participant.vars["mitigation_cost_this_scenario"] = self.session.vars["mitigation_cost"][self.mitigate]
            self.participant.vars["cumulative_payoff"] -= self.participant.vars["mitigation_cost_this_scenario"]
            self.participant.vars["mitigated_this_scenario"] = self.mitigate
        elif self.mitigate == 0:
            self.participant.vars["mitigation_cost_this_scenario"] = self.session.vars["mitigation_cost"][self.mitigate]
            # is zero
            self.participant.vars["mitigated_this_scenario"] = 0

    def new_scenario_method(self):
        for m in range(0, 5):
            self.participant.vars["reduced_deductible"][m] = \
                self.participant.vars["reduced_damage"][m] * self.deductible
        # after start of new scenario set premium to premium with 0 discount, did not work in reset payoffs
        self.participant.vars["premium"] = self.participant.vars["premium_discounted"][0]
        self.participant.vars["deductible_percent"] = int(100 * self.deductible)
        # int to get rid of the decimals of the float that is p.deductible
        self.participant.vars["deductible_ecu_this_scenario"] = Constants.damage * self.deductible  # initially
        self.participant.vars["floodrisk_percent"] = self.risk
        self.participant.vars["cumulative_payoff"] = Constants.initial_endowment
        # resetting cumulative payoff to initial endowment
        self.participant.vars["mitigated_this_scenario"] = 999  # new scenario
        self.participant.vars["in_scenario"] = True
        self.participant.vars["mitigated_before"] = 0
        self.participant.vars["reduced_damage_this_scenario"] = Constants.damage

    def set_payoff(self):
        # SET PREMIUM #######################

        if self.mitigate is None:  # set premium for first year
            self.participant.vars["premium"] = self.participant.vars["premium_discounted"][0]
        elif self.mitigate > 0:  # mitigated this scenario
            #  NO DISCOUNT #####################
            if not self.participant.vars["has_discount"]:
                self.participant.vars["premium"] = self.participant.vars["premium_discounted"][0]
            # DISCOUNT ########################
            elif self.participant.vars["has_discount"]:
                self.participant.vars["premium"] = self.participant.vars["premium_discounted"][self.mitigate]
        # SET PREMIUM * JAAR
        self.participant.vars["total_premium"] = self.participant.vars["premium"]*Constants.jaar
        # SET MITIGATION COST AND REDUCED DAMAGE ###############
        if 0 < self.mitigate <= 4:
            self.participant.vars["reduced_damage_this_scenario"] = \
                self.participant.vars["reduced_damage"][self.mitigate]
            self.mitigation_cost = self.session.vars["mitigation_cost"][self.mitigate]
        else:
            self.mitigation_cost = 0  # initially
            self.participant.vars["reduced_damage_this_scenario"] = Constants.damage
        self.participant.vars["deductible_ecu_this_scenario"] = \
            self.participant.vars["reduced_damage_this_scenario"] * self.deductible


    def set_max_payoff(self):
        if self.participant.vars["treatment"] == "baseline":
            self.participant.vars["max_payoff"] = (Constants.initial_endowment - Constants.jaar *
                                                   ((1 - Constants.deductible) * float(Constants.risk) * 0.01 *
                                                    Constants.damage)) * self.participant.vars["conversion"]
        else:
            self.participant.vars["max_payoff"] = Constants.initial_endowment * self.participant.vars["conversion"]


    def save_payoff(self):
        self.participant.vars["payoff_scenario1"] = self.participant.vars["cumulative_payoff"]

    def save_final_payoffs(self):

        self.payoff_scenario1 = self.participant.vars["payoff_scenario1"]

        self.participant.payoff = self.payoff_scenario1*0.01
        self.participant.vars["payoff_small"] = max(self.payoff_scenario1.to_real_world_currency(self.session)*0.01,
                                                    c(0).to_real_world_currency(self.session))

    def in_scenario(self):
        if self.round_number == Constants.num_start_pages + Constants.num_test_years:
            self.scenario_nr = 0
            return True
        elif self.round_number == Constants.num_start_pages + Constants.num_test_years + Constants.num_def_years:
            self.scenario_nr = 1
            return True
        else:
            return False
