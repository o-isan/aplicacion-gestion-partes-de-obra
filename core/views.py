from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Part
from .serializers import PartSerializer
from .forms import PartForm


# ─── DRF API ViewSet ────────────────────────────────────────────────

class PartViewSet(viewsets.ModelViewSet):
    serializer_class = PartSerializer

    def get_queryset(self):
        return Part.objects.filter(is_deleted=False).select_related(
            'project',
            'canal',
            'responsible_employee',
            'substitute_responsible',
            'ground'
        ).prefetch_related(
            'partmachinery_set',
            'excesshoursjustification_set'
        )

    def destroy(self, request, *args, **kwargs):
        part = self.get_object()
        part.is_deleted = True
        part.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ─── Template-based Views ───────────────────────────────────────────

class PartListView(View):
    def get(self, request):
        parts = Part.objects.filter(is_deleted=False).select_related(
            'project', 'canal', 'responsible_employee', 'ground'
        ).order_by('-registration_date_utc')
        return render(request, 'core/list.html', {'parts': parts})


class PartCreateView(View):
    def get(self, request):
        form = PartForm(initial={'is_deleted': False})
        return render(request, 'core/add.html', {'form': form})

    def post(self, request):
        form = PartForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('part_list')
        return render(request, 'core/add.html', {'form': form})


class PartUpdateView(View):
    def get(self, request, pk):
        part = get_object_or_404(Part, pk=pk, is_deleted=False)
        form = PartForm(instance=part)
        return render(request, 'core/edit.html', {'form': form, 'part': part})

    def post(self, request, pk):
        part = get_object_or_404(Part, pk=pk, is_deleted=False)
        form = PartForm(request.POST, instance=part)
        if form.is_valid():
            form.save()
            return redirect('part_list')
        return render(request, 'core/edit.html', {'form': form, 'part': part})


class PartDeleteView(View):
    def get(self, request, pk):
        part = get_object_or_404(Part, pk=pk, is_deleted=False)
        return render(request, 'core/delete.html', {'part': part})

    def post(self, request, pk):
        part = get_object_or_404(Part, pk=pk, is_deleted=False)
        part.is_deleted = True
        part.save()
        return redirect('part_list')
