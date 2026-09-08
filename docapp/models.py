from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.


class BotUser(models.Model):
    class Role(models.TextChoices):
        USER = "USER", "User"
        SUPPORT = "SUPPORT", "Support"
        ADMIN = "ADMIN", "Admin"
    user_id = ArrayField(
        models.CharField(max_length=100),
        default=list,
        blank=True,
        help_text="List of user IDs from different platforms (e.g., Telegram, WhatsApp)"
    )
    phone_number = models.CharField(max_length=20, unique=True, null=True,blank=True)
    display_name = models.CharField(max_length=150,null=True,blank=True)
    email = models.EmailField(unique=True, null=True,blank=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
        help_text="Role of the user in the system"
    )


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    
class System(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name



class ProblemSolution(models.Model):
    title = models.CharField(max_length=255)
    problem = models.TextField()
    cause = models.TextField(blank=True)
    solution = models.TextField()
    system = models.ForeignKey(System,on_delete=models.SET_NULL,null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rawText = models.TextField(blank=True)
    aiSolution = models.TextField(blank=True)
    aiSolutionStatus = models.BooleanField(default=False)
    reported_by = models.ForeignKey(
        BotUser,
        on_delete=models.SET_NULL,
        null=True,
        related_query_name='reported_problems'
    )
    solved_by = models.ForeignKey(
        BotUser,
        on_delete=models.SET_NULL,
        null=True,
        related_query_name='solved_problems',
        help_text="User who solved the problem",
        related_name='solved_problems'
    )
    solution_status = models.CharField(
        max_length=20,
        choices=[
            ('unsolved', 'Unsolved'),
            ('in_progress', 'In Progress'),
            ('solved', 'Solved')
        ],
        default='unsolved',
        help_text="Status of the solution"
    )
    


    

    