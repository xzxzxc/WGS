from django.views import generic
from .models import Dir, File


class IndexView(generic.ListView):
    template_name = 'links/index.html'
    context_object_name = 'dirs'

    def get_queryset(self):
        return Dir.objects.all()


class DetailView(generic.TemplateView):
    template_name = 'links/index.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['dirs'] = Dir.objects.all()
        context['dir'] = Dir.objects.get(pk=kwargs['pk'])
        context['files'] = File.objects.filter(dir=context['dir'])
        return context

