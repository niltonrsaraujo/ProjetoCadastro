from django import forms

class ConfigurationForm(forms.Form):
    num_variables = forms.IntegerField(label="Número de Variáveis", min_value=1)
    num_constraints = forms.IntegerField(label="Número de Restrições", min_value=1)
    objective_type = forms.ChoiceField(
        label="Tipo de Problema",
        choices=[('maximize', 'Maximizar'), ('minimize', 'Minimizar')]
    )

class CoefficientsForm(forms.Form):
    # Este formulário será gerado dinamicamente na view com base nas configurações.
    pass
