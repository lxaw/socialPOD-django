##########################################
# Default dj imports
##########################################
from django.db import models
from django.utils import timezone

##########################################
# Dj url imports
##########################################
from django.urls import reverse

##########################################
# Dj slugs
##########################################
from django.template.defaultfilters import slugify

##########################################
# Outside libraries
##########################################
import datetime

# Create your models here.

# other needed models
from users.models import CustomUser

##########################################
# Models related to requests for help
##########################################
class HelpRequest(models.Model):
	# associate with user
	author = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name = "created_request_help_set")
	# associate with a title
	title = models.CharField(max_length=200,null=False)
	# associate with text
	text_content = models.CharField(max_length = 300)
	# associate with tags
	tags = models.CharField(max_length = 300,null=True)

	# store date of publication
	pub_date = models.DateTimeField(default=timezone.now)

	# associate with the user that is to help 
	responded_users = models.ForeignKey(CustomUser,null=True,on_delete=models.CASCADE,related_name = "responded_request_help_set")

	# slug field
	slug = models.SlugField(null=False)

	# what needs to be unique together
	# ie, cannot have user "test" create request titled "help"
	# twice
	class Meta:
		unique_together = [['author','title']]
	
	def boolWasRespondedTo(self):
		return (self.responded_users != None)

	# what to call when save model
	def save(self, *args, **kwargs):
		if not self.id:
			# newly created obj, so set slug
			self.slug = slugify(self.title)

		super(HelpRequest,self).save(*args, **kwargs)

	# return the url associated with it
	# this is the url for viewing the request
	def get_absolute_url(self):
		return reverse('newsfeed:detail_help_request',kwargs={"slug":self.slug,
			"username":self.author.username}
			)
	
	def get_parsed_tags(self):
		return [i for i in self.tags.split("-")]

	# check if created within day amount
	def boolWithinXDays(self,intDays):
		now = timezone.now()
		return now - datetime.timedelta(days=intDays) <= self.pub_date <= now
	
	def __str__(self):
		return self.title

##########################################
# Models related to yes no accept requests
##########################################

class HelpRequestOffer(models.Model):
	# associate with user
	author = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="help_request_offer_set")
	# text associated with the message
	text_content = models.CharField(max_length=300)
	# store date of poub
	pub_date = models.DateTimeField(default=timezone.now)
	# associate with a request for help
	help_request = models.ForeignKey(HelpRequest,on_delete=models.CASCADE,related_name="help_request_offer_set")
	# if accepted go true
	is_accepted = models.BooleanField(default=False)

	def get_absolute_url(self):
		return reverse('newsfeed:detail_help_request_offer',kwargs={'id':self.id})

	def boolIsAccepted(self):
		# check if someone accepted offer
		return self.is_accepted
	
	def __str__(self):
		return "Help offer by \"{}\" for \"{}\"".format(self.author.username,self.help_request.title)