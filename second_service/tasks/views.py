from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .tasks import run_acrobot, run_cartpole, run_mountaincar, run_mountaincar_continuous, run_pendulum
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def start_acrobot(self, request):
        run_acrobot.delay()
        return Response({"status": "started"})

    @action(detail=False, methods=['post'])
    def start_cartpole(self, request):
        run_cartpole.delay()
        return Response({"status": "started"})

    @action(detail=False, methods=['post'])
    def start_mountaincar(self, request):
        run_mountaincar.delay()
        return Response({"status": "started"})

    @action(detail=False, methods=['post'])
    def start_mountaincar_continuous(self, request):
        run_mountaincar_continuous.delay()
        return Response({"status": "started"})

    @action(detail=False, methods=['post'])
    def start_pendulum(self, request):
        run_pendulum.delay()
        return Response({"status": "started"})
