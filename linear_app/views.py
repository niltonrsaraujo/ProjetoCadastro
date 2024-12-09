from django.shortcuts import render, redirect
from .forms import ConfigurationForm, CoefficientsForm
from pulp import LpMaximize, LpMinimize, LpProblem, LpVariable


def configure_problem(request):
    if request.method == "POST":
        form = ConfigurationForm(request.POST)
        if form.is_valid():
            # Salvar configurações na sessão
            request.session['num_variables'] = form.cleaned_data['num_variables']
            request.session['num_constraints'] = form.cleaned_data['num_constraints']
            request.session['objective_type'] = form.cleaned_data['objective_type']
            return redirect('input_data')
    else:
        form = ConfigurationForm()
    return render(request, 'linear_app/configure_problem.html', {'form': form})


def input_data(request):
    num_variables = request.session.get('num_variables')
    num_constraints = request.session.get('num_constraints')

    if request.method == "POST":
        # Coletar coeficientes da função objetivo e das restrições
        coefficients = {key: value for key, value in request.POST.items() if key.startswith('coef')}
        constraints = {key: value for key, value in request.POST.items() if key.startswith('constraint')}
        request.session['coefficients'] = coefficients
        request.session['constraints'] = constraints
        return redirect('results')

    # Gerar campos dinâmicos
    return render(request, 'linear_app/input_data.html', {
        'num_variables': range(1, num_variables + 1),
        'num_constraints': range(1, num_constraints + 1)
    })


def results(request):
    num_variables = request.session.get('num_variables')
    num_constraints = request.session.get('num_constraints')
    coefficients = request.session.get('coefficients')
    constraints = request.session.get('constraints')
    objective_type = request.session.get('objective_type')

    # Resolver problema com PuLP
    problem = LpProblem(name="linear-programming-problem",
                        sense=LpMaximize if objective_type == 'maximize' else LpMinimize)
    variables = [LpVariable(f"x{i}", lowBound=0) for i in range(1, num_variables + 1)]

    # Adicionar função objetivo
    problem += sum(
        float(coefficients[f"coef_{i}"]) * variables[i - 1] for i in range(1, num_variables + 1)), "Objective"

    # Adicionar restrições
    for j in range(1, num_constraints + 1):
        constraint_expr = sum(
            float(constraints[f"constraint_{j}_coef_{i}"]) * variables[i - 1] for i in range(1, num_variables + 1)
        )
        problem += constraint_expr <= float(constraints[f"constraint_{j}_limit"])

    # Resolver
    problem.solve()

    # Preparar resultados
    results = {
        'status': problem.status,
        'objective_value': problem.objective.value(),
        'variables': {v.name: v.value() for v in variables},
    }

    return render(request, 'linear_app/results.html', {'results': results})
