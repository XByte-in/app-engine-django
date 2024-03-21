from django.db import models
from django.core.validators import MinLengthValidator
# Create your models here.

class Tag(models.Model):
    caption=models.CharField(max_length=50)

    def __str__(self):
        return f"{self.caption}"
    
class Author(models.Model):
    fname=models.CharField(max_length=25)
    lname=models.CharField(max_length=25)
    email=models.EmailField()

    def __str__(self):
        return f"{self.fname} {self.lname}"

class Post(models.Model):
    title=models.CharField(max_length=25)
    excerpt=models.CharField(max_length=50)
    # image=models.CharField(max_length=25)
    image = models.ImageField(upload_to="posts")
    dated=models.DateField(auto_now=True)
    content=models.TextField(validators=[MinLengthValidator(10)])
    slug=models.SlugField(unique=True)
    tags=models.ManyToManyField(Tag)
    author=models.ForeignKey(Author,on_delete=models.SET_NULL,null=True,related_name="posts")

    def __str__(self):
        return f"{self.title} | {self.excerpt}"
    

class Comment(models.Model):
    username=models.CharField(max_length=50)
    useremail=models.EmailField()
    text = models.TextField()
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
