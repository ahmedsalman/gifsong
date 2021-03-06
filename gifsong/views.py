#! /usr/bin/env python2.7
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.forms import ModelForm
from django.db.models import Q

from gifsong.models import gifsong

class GifSongForm(ModelForm):
    class Meta:
        model = gifsong
        fields = ['image_url', 'audio_url']

class showgifsong(TemplateView):
    template_name = 'showsong.html'

    def get(self, request, *args, **kwargs):
        gvidid = request.GET.get('gvid')
        nsfw = request.GET.get('nsfw')
        agifsong = None

        if(gvidid):
            agifsong = gifsong.objects.get(id=gvidid)

        if (agifsong == None):
            if(nsfw == None):
                sfw = gifsong.objects.all().filter(Q(sfwness=1) | Q(sfwness=3)).order_by('?')
                if(sfw):
                    agifsong = sfw[0]
            if(nsfw):
                agifsong = gifsong.objects.order_by('?')[0]

        context = {
            'song' : agifsong,
        }

        return self.render_to_response(context)

class addgifsong(TemplateView):
    template_name = 'createsong.html'

    def get(self, request, *args, **kwargs):

        form = GifSongForm()

        context = {
            'form' : form,
        }

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = GifSongForm(request.POST)
        if form.is_valid():
            song = form.save()
            return redirect('/show?gvid=' + str(song.id))

        return self.render_to_response({'form': GifSongForm() })
