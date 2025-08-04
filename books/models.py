from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField()
    average_rating = models.FloatField(default=0.0)
    

    def __str__(self):
        return self.title

    def update_average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            self.average_rating = sum(r.rating for r in reviews) / reviews.count()
        else:
            self.average_rating = 0.0
        self.save()


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} - {self.book.title}"


class Favorite(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='favorites')
    user_name = models.CharField(max_length=255)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['book', 'user_name']  
    
    def __str__(self):
        return f"{self.user_name} - {self.book.title}"


