import numpy as np

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from scipy.stats import norm

from forecaster.models import Forecast


def index(request):
    """The index is the homepage and lists all the stored forecasts and links
    to a new forecast creation page.
    """

    return render(request, "index.html")


def create_forecast(request):
    """The create forecast page has a drawing area to draw probabilistic
    distributions.

    Currently, only the normal distribution is implemented.

    Hitting the delete key undos the last action.

    There is a title field and a save button, which stores the forecast in the
    database.
    """

    return render(request, "new.html")


def create(request):
    if request.method == "POST":
        params = request.POST

        Forecast.objects.create(
            title=params.get("title", "no title"),
            mean=float(params.get("mean", 50)),
            variance=float(params.get("variance", 10)),
        )

        return HttpResponse("success")


def normal_distribution(request):
    params = request.GET

    x = np.linspace(0, 100, 21)
    mean = float(params.get("mean", 50))
    variance = float(params.get("variance", 10))
    data = {
        "labels": x.tolist(),
        "y": (norm.pdf(x, mean, variance) * 100).tolist(),
    }

    return JsonResponse(data=data)


def recent(request):
    forecasts = Forecast.objects.all().order_by("-created")[:10]

    normals = np.ones(shape=[len(forecasts), 21])
    titles = []
    x = np.linspace(0, 100, 21)

    for index, forecast in enumerate(forecasts):
        normals[index] *= (norm.pdf(x, float(forecast.mean), float(forecast.variance)) * 100)
        titles.append(forecast.title)

    data = {
        "labels": x.tolist(),
        "y": normals.tolist(),
        "titles": titles,
    }

    return JsonResponse(data=data)
