from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from polls.models import Choice, Poll
# Create your views here.
"""
	Generic View
		Needs to know what model it will be acting upon
		Provided using the model attribute
	ListView	display a list of objects
			Uses default template: <app_name>/<model name>_list.html
			Use template_name to tell ListView to use "polls/index.html" template
			??Context Variable??
	DetailView	display a detail page for a particular type of object
			expects the primary key value captured from the URL to be called "pk",
			so we've changed poll_id to pk for the generic views
			by default, DV generic view uses a template called:
				<app_name>/<model name>_detail.html
	In previous parts of the tutorial, the templates have been provided with a context that
	contains the poll and latest_poll_list context variables
	
	client = Client()
	response = client.get('/polls')
	response.content
	response.context
	response.context_data
		this extracts the data the view (IndexView) places into the context
		Poll.objects.filter(pub_date__lte=timezone.now()).order_by('pub_date'[:5]
"""
class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_poll_list'
	
	"""
	return the last five published polls (not including those set to be
	published in the future
	"""
	def get_queryset(self):
		#return Poll.objects.order_by('-pub_date')[:5]
		return Poll.objects.filter(pub_date__lte=timezone.now()
			).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Poll
	template_name = 'polls/detail.html'
	def get_queryset(self):
		"""
		excludes any polls that aren't published yet
		"""
		return Poll.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
	model = Poll
	template_name = 'polls/results.html'

# Create your views here.
def index(request):
	#return HttpResponse("Hello, world. You're at the poll index.")
	#latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
	#output = ', '.join([p.question for p in latest_poll_list])
	#return HttpResponse(output)
	
	#latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
	#template = loader.get_template('polls/index.html')
	#context = RequestContext(request, {
	#	'latest_poll_list': latest_poll_list,
	#	})
	#return HttpResponse(template.render(context))
	"""
	the context is passed to polls/index.html
	the context is a dictionary mapping template variable names to
	python objects
	"""
	latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
	context = {'latest_poll_list': latest_poll_list}
	return render(request,'polls/index.html', context)

def detail(request, poll_id):
	#return HttpResponse("You're looking at poll %s." % poll_id)
	#try:
	#	poll = Poll.objects.get(pk=poll_id)
	#except Poll.DoesNotExist:
	#	raise Http404
	#return render(request, 'polls/detail.html', {'poll': poll})
	poll = get_object_or_404(Poll,pk=poll_id)
	return render(request,'polls/detail.html',{'poll': poll})

def results(request, poll_id):
	#return HttpResponse("You're lookiing at the results of poll %s." % poll_id)
	poll = get_object_or_404(Poll,pk=poll_id)
	return render(request,'polls/results.html', {'poll': poll})

def vote(request, poll_id):
	#return HttpResponse("You're voting on poll %s." % poll_id)
	p = get_object_or_404(Poll, pk=poll_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError,Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {
			'poll': p,
			'error_message': "You didn't select a choice.",
			})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if
		# user hits the Back button
		return HttpResponseRedirect(reverse('polls:results',args=(p.id,)))
