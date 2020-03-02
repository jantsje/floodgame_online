from . import models
from ._builtin import Page
from .models import Constants
from floodgame_online.extra_pages import Check as UnderstandingQuestionsPage
from django.http.response import HttpResponseRedirect


class Helaas(Page):

    def dispatch(self, request, *args, **kwargs):
        from otree.models import Participant
        participant = Participant.objects.get(code=kwargs.get('participant_code'))
        if request.method == 'GET':
            adres = 'https://www.websiteonlinepanel.com/id=' + str(participant.label)
            # screen-out (not in target group)
            return HttpResponseRedirect(adres)
        return super(Page, self).dispatch(request, *args, **kwargs)

    form_model = 'player'

    def is_displayed(self):
        return self.round_number == 1 and not self.player.participant.vars["doelgroep"] and not \
            self.session.vars["quotafull"]


def vars_for_all_templates(self):
    player = self.player
    participant = self.participant
    return_vars = {'progress': progress(self),
                   'cumulative_payoff': participant.vars["cumulative_payoff"],
                   'risk': player.risk, 'round': player.round_number,
                   'scenario_nr': player.scenario_nr,
                   'insurance_choice': participant.vars["insurance_choice"],
                   'total_premium': participant.vars["total_premium"],
                   'has_discount': participant.vars["has_discount"],
                   'is_voluntary': participant.vars["is_voluntary"],
                   'language_code': self.session.config['language']
                   }
    return_vars.update(self.player.vars_for_scenarios())
    return return_vars


def progress(p):
    progressrel = p.round_number/Constants.num_rounds*100
    return(str(progressrel))
    # return str(locale.atof(str(progressrel)))
    # this looks really bad but it has to do with the NL language settings in Django
    # and the fact that the progressbar does not work with comma separators for decimals


class spelpagina(Page):
    def get_form_fields(self):
        return self.form_fields + ['opened']


class Welkom(Page):
    form_model = 'player'
    form_fields = ['opened', 'koopwoning', 'postcode_cijfers', 'postcode_letters']

    def vars_for_template(self):
        return {'participation_fee': self.session.config['participation_fee'],
                'page_title': ''}

    def is_displayed(self):
        self.player.participant_started()
        return self.round_number == 1 and not self.session.vars["quotafull"]

    def before_next_page(self):
        self.player.browser = self.request.META.get('HTTP_USER_AGENT')
        self.player.set_max_payoff()
        self.player.set_treatment()
        self.player.store_koopwoning()
        # if not self.player.participant.vars["doelgroep"]:
        #     return render(request)


class Full(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.participant.vars["quotafull"]

    def dispatch(self, request, *args, **kwargs):
        from otree.models import Participant
        participant = Participant.objects.get(code=kwargs.get('participant_code'))
        if request.method == 'GET':
            adres = 'https://www.websiteonlinepanel.com/id=' + str(participant.label)
            # quota-full link here
            return HttpResponseRedirect(adres)
        return super(Page, self).dispatch(request, *args, **kwargs)


class Start(Page):
    form_model = 'player'

    def before_next_page(self):
        if self.round_number == 2:
            self.player.store_follow_up()

    def get_form_fields(self):
        if self.round_number == 1:
            return ['gender', 'age', 'edu', 'anders_text']
        elif self.round_number == 2:
            return ['flood_prone', 'evacuated', 'damaged', 'flood_prob']
        elif self.round_number == 3:
            if self.player.participant.vars["evacuated_text_needed"]:
                return ['evacuated_imagine', 'climate_change', 'availability',
                        'waterdiepte', 'regret_before']
            else:
                return ['climate_change', 'availability',
                        'waterdiepte', 'regret_before']
        elif self.round_number == 4:
            return ['income', 'home', 'expected_damage', 'floor', 'anders_text']
        elif self.round_number == 5:
            return['insurance', 'insurances', 'anders_text']

    def is_displayed(self):
        return self.round_number <= Constants.num_start_pages and self.player.participant.vars["doelgroep"] and not \
            self.participant.vars["quotafull"]


class Einde(Page):
    form_model = 'player'

    def before_next_page(self):
        if self.round_number == 7 or self.round_number == 14:
            self.player.store_follow_up()
        elif self.round_number == 15:
            self.player.store_complete()

    def get_form_fields(self):
        if self.round_number == 7:
            return['measures', 'neighbors', 'anders_text']
        elif self.round_number == 8:
            if self.participant.vars["neighbors_needed"]:
                return['neighbors_measures', 'anders_text']
            else:
                return[]
        elif self.round_number == 9:
            return ['risk_qual', 'time_qual', 'risk_qual_spec']
        elif self.round_number == 10:
            return ['perceived_efficacy', 'self_efficacy', 'perceived_cost']
        elif self.round_number == 11:
            if self.player.participant.vars["flooded"]:
                return ['worry', 'trust', 'regret1', 'norm1', 'norm2']
            else:
                return ['worry', 'trust', 'regret2', 'norm1', 'norm2']
        elif self.round_number == 12:
            return['control', 'control2', 'control3', 'control4', 'concern']
        elif self.round_number == 13:
            return ['exact_flood_risk_perception']
        elif self.round_number == 14:
            return ['difficult', 'explain_strategy', 'cloud', 'cloud2']
        elif self.round_number == 15:
            if self.participant.vars["difficult_text_needed"]:
                return ['difficult_text', 'feedback']
            else:
                return ['feedback']

    def is_displayed(self):
        if self.participant.vars["quotafull"]:
            return False
        else:
            if not self.player.participant.vars["doelgroep"]:
                return False
            elif self.round_number == 8:
                if self.participant.vars["neighbors_needed"]:
                    return True
                else:
                    return False
            else:
                return self.round_number >= 7


class WTP(Page):
    form_model = 'player'
    form_fields = ['accept_fair']

    def vars_for_template(self):
        return {'page_title': 'Wilt u zich verzekeren?'}

    def is_displayed(self):
        return self.participant.vars["is_voluntary"] and self.round_number == 6 and \
               self.player.participant.vars["doelgroep"] and not \
               self.participant.vars["quotafull"]

    def before_next_page(self):
        self.player.set_insurance()


class WTP2(Page):
    form_model = 'player'
    form_fields = ['accept_lower']

    def vars_for_template(self):
        return {'page_title': 'Wilt u zich verzekeren voor een lagere premie?'}

    def is_displayed(self):
        return self.participant.vars["is_voluntary"] and self.round_number == 6 and \
               self.player.participant.vars["doelgroep"] and not self.player.accept_fair and not \
               self.participant.vars["quotafull"]

    def before_next_page(self):
        self.player.set_insurance()


class WTP3(Page):
    form_model = 'player'
    form_fields = ['wtp']

    def is_displayed(self):
        return self.participant.vars["is_voluntary"] and self.round_number == 6 and \
               self.player.participant.vars["doelgroep"] and not \
               self.participant.vars["quotafull"]

    def vars_for_template(self):
        return {'max_premium': Constants.monthly_subsidized - 1,
                'max_premium_fair': Constants.fair - 1,
                'page_title': 'Hoeveel premie wilt u maximaal betalen?'}
    #
    # def before_next_page(self):
    #     self.player.set_insurance()


class UwVerzekering(Page):
    form_model = 'player'
    form_fields = ['opened']


    def is_displayed(self):
        return self.participant.vars["is_voluntary"] and self.round_number == 6 and \
               self.player.participant.vars["doelgroep"] and not \
               self.participant.vars["quotafull"]

    def vars_for_template(self):
        return{'page_title': 'Uw verzekering'}


class Scenario(Page):
    form_model = 'player'

    def get_form_fields(self):
        return self.form_fields + ['opened']

    def vars_for_template(self):
        return {'max_payoff': self.participant.vars["max_payoff"]}

    def is_displayed(self):
        return self.round_number == Constants.num_start_pages and self.player.participant.vars["doelgroep"] and not \
            self.participant.vars["quotafull"]

    def before_next_page(self):
        self.player.new_scenario_method()


class Instructies(Page):
    form_model = 'player'

    def get_form_fields(self):
        return self.form_fields + ['opened']

    def is_displayed(self):
        return self.round_number == Constants.num_start_pages and self.player.participant.vars["doelgroep"] and not \
            self.participant.vars["quotafull"]


class Instructies3(Page):
    form_model = 'player'

    def get_form_fields(self):
        return self.form_fields + ['opened']

    def is_displayed(self):
        return self.round_number == Constants.num_start_pages + 1 and \
               self.player.participant.vars["doelgroep"] and not self.participant.vars["quotafull"]

    def before_next_page(self):
        self.player.new_scenario_method()

    def vars_for_template(self):
        return{'page_title': 'Schadebeperkende maatregelen'}


class NieuwScenario(spelpagina):
    form_model = 'player'

    def before_next_page(self):
        self.player.opened_instructions()

    def is_displayed(self):
        return self.player.in_scenario() and self.player.participant.vars["doelgroep"] and not \
            self.participant.vars["quotafull"]

    def vars_for_template(self):
        return{'page_title': 'Scenario'}


class Begripsvragen_(UnderstandingQuestionsPage):
    page_title = 'Begripsvragen'
    set_correct_answers = False  # APPS_DEBUG
    form_model = 'player'
    form_field_n_wrong_attempts = 'understanding_questions_wrong_attempts'

    def get_questions(self):
        return self.player.get_questions_method()

    def before_next_page(self):
        self.player.opened_instructions()
        self.player.new_scenario_method()

    def is_displayed(self):
        return self.round_number == Constants.num_start_pages + Constants.num_test_years and \
               self.player.participant.vars["doelgroep"] and not self.participant.vars["quotafull"]


class Premie(spelpagina):
    form_model = 'player'
    form_fields = ['pay_premium']

    def is_displayed(self):
        if self.participant.vars["quotafull"]:
            return False
        elif not self.participant.vars["has_insurance"]:
            return False
        else:
            return self.player.in_scenario() and self.player.participant.vars["doelgroep"]

    def before_next_page(self):
        self.player.pay_premium_method()
        self.player.opened_instructions()

    def vars_for_template(self):
        return {'page_title': 'Betaal uw premie'}


class Keuze(spelpagina):
    form_model = 'player'
    form_fields = ['mitigate']

    def vars_for_template(self):
        vars_for_this_template = self.player.vars_for_invest()
        vars_for_this_template.update({'page_title': "Investering"})
        return vars_for_this_template

    def before_next_page(self):
        self.player.set_payoff()
        self.player.pay_mitigation_method()
        self.player.opened_instructions()

    def is_displayed(self):
        return self.player.in_scenario() and self.player.participant.vars["doelgroep"] and not \
            self.participant.vars["quotafull"]


class Overstromingskans(spelpagina):
    form_model = 'player'

    def is_displayed(self):
        return self.player.in_scenario() and self.player.participant.vars["doelgroep"] and not \
            self.participant.vars["quotafull"]

    def get_form_fields(self):
        if self.player.flooded and self.player.participant.vars["has_insurance"]:
            # only show button to pay deductible if player is flooded and has insurance
            return ['pay_deductible', 'opened']
        elif self.player.flooded and not self.player.participant.vars["has_insurance"]:
            # only show button to pay damage if player is flooded and no insurance was offered
            return ['pay_damage', 'opened']
        else:
            return['opened']

    def vars_for_template(self):
        player = self.player
        d = {'floodnrs': player.floodnrs,
             'items': models.Constants.items,
             'items2': models.Constants.items2,
             'page_title': str('Overstromingen in de afgelopen ' + str(Constants.jaar) + ' jaar')
             }
        return d

    def before_next_page(self):
        self.player.pay_after_flood()
        self.player.save_payoff()
        self.player.opened_instructions()

        if self.player.flooded:
            self.player.participant.vars["flooded"] = True

        if self.player.round_number == Constants.num_start_pages + Constants.num_test_years:
            pass
        else:
            self.player.save_final_payoffs()


class Overzicht(spelpagina):
    form_model = 'player'

    def vars_for_template(self):
        vars_for_this_template = self.player.vars_for_invest()
        vars_for_this_template.update({'page_title': str('Overzicht van de afgelopen ' +
                                                         str(Constants.jaar) + ' jaar')})
        return vars_for_this_template

    def before_next_page(self):
        self.player.opened_instructions()

    def is_displayed(self):
        return self.player.in_scenario() and self.player.participant.vars["doelgroep"] and not \
            self.participant.vars["quotafull"]


class Resultaten(spelpagina):
    form_model = 'player'
    form_fields = ['selected']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds - Constants.num_end_pages and \
               self.player.participant.vars["doelgroep"] and not self.participant.vars["quotafull"]

    def vars_for_template(self):
        vars_for_this_template = self.player.vars_for_payment()
        vars_for_this_template.update({'page_title': ""})
        return vars_for_this_template


class Dank(Page):
    form_model = 'player'

    def vars_for_template(self):
        return {'page_title': 'Hartelijk dank voor uw deelname'}

    def is_displayed(self):
        return self.round_number == 15 and self.player.participant.vars["doelgroep"] and not \
            self.participant.vars["quotafull"]

    def dispatch(self, request, *args, **kwargs):
        from otree.models import Participant
        participant = Participant.objects.get(code=kwargs.get('participant_code'))
        if request.method == 'GET':
            adres = 'https://www.websiteonlinepanel.com/id=' + str(participant.label)
            # complete link here
            return HttpResponseRedirect(adres)
        return super(Page, self).dispatch(request, *args, **kwargs)


page_sequence = [
    Welkom,
    Full,
    Helaas,
    Start,
    Scenario,
    Instructies,
    WTP,
    WTP2,
    WTP3,
    UwVerzekering,
    Instructies3,
    NieuwScenario,
    Keuze,
    Premie,
    Overstromingskans,
    Overzicht,
    Begripsvragen_,
    Resultaten,
    Einde,
    Dank
]
