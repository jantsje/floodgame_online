from otree.api import (
    models, widgets as widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer
)
from django import forms

YESNO = ["Ja", "Nee"]

regret_before = models.StringField(label="Wat vindt u van de volgende bewering?", help_text=
                                              "Ik zou spijt hebben wanneer mijn huis zou overstromen en ik "
                                              "geen maatregelen had genomen",
                                 choices=["Helemaal me eens", "Mee eens", "Niet mee eens/niet mee oneens",
                                          "Niet mee eens", "Helemaal niet mee eens"])

control = models.StringField(
    label="Als ik krijg wat ik wil, is dat meestal omdat ik geluk heb.",
blank=True)

control2 = models.StringField(
    label="Het is niet altijd verstandig voor mij om ver vooruit te plannen omdat veel zaken "
                 "afhankelijk zijn van geluk.", blank=True)
control3 = models.StringField(
    label="Ik geloof dat er een aantal maatregelen zijn die mensen kunnen nemen om de risico's "
                 "die zij lopen te verkleinen.", blank=True)
control4 = models.StringField(
    label="Ik kan bijna volledig bepalen wat er zal gebeuren in mijn leven.", blank=True)

difficult = models.StringField(
        label="Hoe makkelijk of moeilijk vond u het om een keuze te maken in het scenario?",
        choices=["Heel makkelijk", "Makkelijk", "Niet makkelijk/Niet moeilijk", "Moeilijk", "Heel moeilijk"])
        # note: without this default option, an empty checkbox will be displayed that is initially selected)

difficult_text = models.LongStringField(
    widget=forms.Textarea(attrs={'rows':3, 'cols':100}),
    label="Kunt u uitleggen wat het scenario moeilijk maakte voor u?")

explain_strategy = models.LongStringField(
    widget=forms.Textarea(attrs={'rows':3, 'cols':100}),
    label="Kunt u in het kort uitleggen hoe uw beslissingen tot stand kwamen in het scenario?")

age = models.PositiveIntegerField(label="Wat is uw leeftijd?",
                                  help_text="jaar", min=18, max=120)
gender = models.StringField(
    label="Ik ben een:",
    choices=["Man", "Vrouw"], widget=widgets.RadioSelectHorizontal,
    default="")
# children = models.IntegerField(label="Hoeveel thuiswonende kinderen heeft u?",
#                                max=20, blank=True)

flood_prob = models.StringField(
    label="Hoe groot of klein denkt u dat de kans is dat uw huis overstroomt?",
    choices=["Het overstromingsrisico van mijn huis is 0",
             "Erg laag", "Laag", "Niet laag niet hoog", "Hoog", "Erg hoog",
             "Dat weet ik niet"
    ]
)


waterdiepte = models.StringField(
    label="Stel dat uw buurt zou overstromen, hoe hoog denkt u dat het water dan zou komen in uw woning?",
    choices = ["Het water zou mijn woning niet bereiken",
               "Laag (1-10 cm)",
               "Redelijk (10-50 cm)",
               "Behoorlijk (50-100 cm)",
               "Hoog (1-2 meter)",
               "Heel hoog (hele verdieping overstroomd)"]
)


measures = models.StringField(widget=forms.CheckboxSelectMultiple,
                            label="Heeft u één of meerdere van de volgende maatregelen "
                                         " genomen om uw huis tegen overstromingsschade te beschermen?",
                            blank=True)

anders_text = models.StringField(blank=True)

neighbors = models.StringField(label="Kent u mensen in uw directe omgeving die "
                                          "(overstromings)schadebeperkende maatregelen "
                                          "hebben genomen voor hun huis?",
                             choices=YESNO,
                             widget=widgets.RadioSelectHorizontal)

neighbors_measures = models.StringField(widget=forms.CheckboxSelectMultiple,
                                label="Kunt u aangeven wat uw relatie is tot de persoon in uw omgeving"
                                             " die schadebeperkende maatregelen heeft genomen?",
                                blank=True, help_text="Ik ben zijn/haar ...")


income = models.StringField(
    label="Wat is (ongeveer) het netto maandelijks inkomen van uw gehele huishouden?",
    choices=["Minder dan €499", "Tussen €500 en €999", "Tussen €1000 en €1499",
             "Tussen €1500 en €1999", "Tussen €2000 en €2499", "Tussen €2500 en €2999",
             "Tussen €3000 en €3499", "Tussen €3500 en €3999", "Tussen €4000 en €4499",
             "Tussen €4500 en €4999", "€5000 of meer", "Dat weet ik niet", "Zeg ik liever niet"])

floor = models.StringField(label="Hoe zou uw huis omschrijven?")
edu = models.StringField(label="Wat is uw hoogst voltooide opleiding?")

postcode = models.StringField(
    label="Wat is uw postcode?",
    blank=True)

postcode_cijfers = models.IntegerField(blank=True)
postcode_letters = models.StringField(blank=True)

insurance = models.StringField(
    label="Wat is uw eigen risico voor uw zorgverzekering van 2018?",
    choices=["385 euro, het minimum vastgesteld door de Nederlandse overheid",
             "485 euro, ik heb het opgehoogd met 100 euro",
             "585 euro, ik heb het opgehoogd met 200 euro",
             "685 euro, ik heb het opgehoogd met 300 euro",
             "785 euro, ik heb het opgehoogd met 400 euro",
             "885 euro, ik heb het opgehoogd met 500 euro (het maximum)",
             "Dat weet ik niet",
             'Ik heb geen Nederlandse zorgverzekering'])

ins = (("tandarts", "Tandartsverzekering"),
       ('aanvullend', "Ander aanvullend pakket in zorgverzekering (o.a. fysiotherapie, bril)"),
       ("inboedel","Inboedelverzekering"),
       ("woonhuis", "Woonhuisverzekering"),
       ("auto","All risk autoverzekering"),
       ("reis", "Doorlopende reisverzekering"),
       ("leven", "Levensverzekering"),
       ("recht", "Rechtsbijstandsverzekering"),
       ("fiets", "Fietsverzekering"),
       ("arbeid", "Arbeidsongeschiktheidsverzekering"),
       ('wa', "Wettelijke aansprakelijkheidsverzekering")
       )

insurances = models.StringField(widget=forms.CheckboxSelectMultiple(choices=ins),
                                label="Kunt u aangeven welke verzekering(en) "
                                             "u heeft op het moment?",
                                blank = True)

feedback = models.LongStringField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 130}),
                            label="Dit is het einde van de vragenlijst. Mocht u opmerkingen hebben, "
                                         "dan kunt u deze hieronder kwijt.",
                            blank=True)

evacuated = models.StringField(label="Bent u ooit geëvacueerd in verband met een dreigende overstroming?",
                             choices=YESNO,
                             widget=widgets.RadioSelectHorizontal, default=""
                             )

evacuated_imagine = models.StringField(
    label="Denkt u dat uw ervaring met evacuatie het makkelijker maakt om voor te stellen dat een overstroming"
                 " in de nabije toekomst plaatsvindt?",
    choices=["Ja, ik kan me nu voorstellen dat een overstroming heel waarschijnlijk is",
             "Nee, ik kan me niet voorstellen dat een overstroming heel waarschijnlijk is",
             "Ik denk niet dat deze ervaring mijn beeld van de waarschijnlijkheid van een overstroming heeft veranderd"],
    )

expected_damage = models.StringField(label="Hoeveel schade aan uw huis en inboedel"
                                                 " denkt u dat een overstroming u zou kosten?",
                                choices=["Minder dan €1,000",
                                  "Tussen €1,000 en €4,999",
                                  "Tussen €5,000 en €9,999",
                                  "Tussen €10,000 en €49,999",
                                  "Tussen €50,000 en €99,999",
                                  "Tussen €100,000 en €499,999",
                                  "€500,000 of meer", "Dat weet ik niet", "Zeg ik liever niet"])

home = models.StringField(label="Wat is ongeveer de marktwaarde van uw huis?",
                         choices=["Minder dan €100,000",
                                  "Tussen €100,000 en €149,999", "Tussen €150,000 en €199,999",
                                  "Tussen €200,000 en €249,999", "Tussen €250,000 en €299,999",
                                  "Tussen €300,000 en €349,999", "Tussen €350,000 en €399,999",
                                  "Tussen €400,000 en €449,999", "Tussen €450,000 en €499,999",
                                  "Tussen €500,000 en €549,999", "Tussen €550,000 en €599,999",
                                  "Tussen €600,000 en €649,999", "Tussen €650,000 en €699,999",
                                  "Tussen €700,000 en €749,999", "Tussen €750,000 en €799,999",
                                  "€800,000 of meer", "Dat weet ik niet", "Zeg ik liever niet"])

flood_prone = models.StringField(
    label="Woont u op dit moment in een gebied dat kan overstromen?",
    choices=[" Ja, ik ben er zeker van dat ik in een risicogebied woon",
             " Ik denk dat ik in een risicogebied woon, maar ik weet het niet zeker",
             " Nee, ik ben er zeker van dat ik niet in een risicogebied woon", " Dat weet ik niet"],
    widget=widgets.RadioSelect,
    default="")

climate_change = models.StringField(
    label="Wat verwacht u dat de gevolgen van klimaatverandering zullen "
                 "zijn voor de kans op een overstroming"
                 " op uw huidige adres?",
    choices=[" Kans op een overstroming zal toenemen", " Kans op een overstroming zal gelijk blijven",
             " Kans op een overstroming zal afnemen", " Dat weet ik niet"],
    )

availability = models.StringField(
    label="Kunt u zich situaties herinneren van uitzonderlijk hoge waterstanden in rivieren "
                 "in de buurt van uw huidige woning?",
    choices=["Ja, ik kan me hoge waterstanden herinneren", "Nee, ik kan me geen hoge waterstanden herinneren"],
    )

damaged = models.StringField(
    label="Heeft u ooit schade gehad als gevolg van een overstroming?",
    choices=YESNO,
    widget=widgets.RadioSelectHorizontal,
    default="")

exact_flood_risk_perception = models.StringField(
    label="Hoe groot denkt u dat de kans op een overstroming is in het gebied waar u woont?",
    help_text="jaar"
)

regret1 = models.StringField(label="Ik had spijt toen ik niet had geinvesteerd in schadebeperkende maatregelen, "
                                        "en in het scenario een overstroming plaatsvond.",
                           blank=True)
regret2 = models.StringField(
    label="Toen in mijn scenario geen overstroming plaatsvond, "
                 "had ik spijt over het betalen voor schadebeperkende maatregelen.",
blank=True)
norm1 = models.StringField(
    label="Ik denk dat "
                 "mensen in mijn directe omgeving een investering in overstromings-"
                 "schadebeperkende maatregelen (door mij) zouden goedkeuren.",
    blank=True)
norm2 = models.StringField(
    label="Ik denk dat mensen in mijn directe omgeving vinden dat ik zou moeten investeren "
                 "in overstromings-"
                 "schadebeperkende maatregelen.",
blank=True)
worry = models.StringField(
    label="Ik maak me zorgen over het gevaar van een overstroming op mijn huidige adres.",
blank=True)
sleep = models.StringField(
    label="Ik zou rustiger slapen als ik een overstromingsverzekering had.")
trust = models.StringField(
    label="Ik ben vol vertrouwen dat de dijken in Nederland goed worden onderhouden.",
blank=True)
trust2 = models.StringField(
    label="Ik heb vol vertrouwen in de technische vaardigheden van overstromingsrisico-beheerders")
concern = models.StringField(
    label="De kans op een overstroming op mijn adres is te klein om me druk over te maken.",
blank=True)
no_info = models.StringField(
    label="Ik zou niet snel informatie zoeken over overstromingsrisico's omdat het veel moeite is"
                 "voor iets wat waarschijnlijk toch nooit gebeurt.")

government = models.StringField(
    label="Ik verwacht dat de overheid mijn schade zal vergoeden als ik word getroffen door een overstroming")
trust_insurer = models.StringField(
    label="Ik vertrouw erop dat mijn schadeverzekeraar het beste met mij voor heeft.")
trust_insurer2 = models.StringField(
    label="Ik vertrouw erop dat mijn schadeverzekeraar doet wat zij zegt."
)

cloud = models.FloatField(
    label="Hoe groot denkt u dat de kans is dat het morgen bewolkt is waar u woont?",
min=0, max=100, help_text ="%")
cloud2 = models.FloatField(
    label="Hoe groot denkt u dat de kans is dat het morgen bewolkt en regenachtig is "
                 "waar u woont?", min=0, max=100, help_text ="%")

time_qual = models.IntegerField(
    label="In hoeverre bent u bereid vandaag geld opzij te zetten "
                 "om hiervan in de toekomst profijt te hebben?"
)

risk_qual = models.IntegerField(
    label="Bent u over het algemeen bereid om risico's te nemen?"
)

risk_qual_spec = models.IntegerField(
    label="Bent u bereid om risico's te nemen als het gaat om voorkomen van schade aan uw huis?"
)

perceived_efficacy = models.StringField(
    label="Hoe effectief denkt u dat investeren in "
                 "(overstromings)schadebeperkende maatregelen zou zijn voor uw woning?",
    choices=["Heel erg effectief",
             "Effectief",
             "Niet effectief/niet ineffectief",
             "Niet effectief",
             "Totaal niet effectief"]
)

self_efficacy = models.StringField(
    label="Hoe makkelijk denkt u dat het is om (overstromings)schadebeperkende"
                 " maatregelen te nemen voor uw woning?",
    choices=["Heel makkelijk", "Makkelijk", "Niet makkelijk/Niet moeilijk", "Moeilijk", "Heel moeilijk"]

)

perceived_cost = models.StringField(
    label = "Hoe duur denkt u dat het is om (overstromings)schadebeperkende"
     " maatregelen te nemen voor uw woning?",
    choices=["Heel duur", "Duur", "Niet duur/Niet goedkoop", "Goedkoop", "Heel goedkoop"]

)