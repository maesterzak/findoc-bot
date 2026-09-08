from django.db import models

# Create your models here.


class BotUser(models.Model):
    class Role(models.TextChoices):
        USER = "USER", "User"
        SUPPORT = "SUPPORT", "Support"
        ADMIN = "ADMIN", "Admin"
    user_id = models.CharField(max_length=100, unique=True, null=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True)
    display_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True, null=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER
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
    aiSolution = models.TextField(blank=True)
    aiSolutionStatus = models.BooleanField(default=False)
    reported_by = models.ForeignKey(
        BotUser,
        on_delete=models.SET_NULL,
        null=True
    )
    solved_by = models.ForeignKey(
        BotUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='solved_problems'
    )
    solution_status = models.CharField(
        max_length=20,
        choices=[
            ('unsolved', 'Unsolved'),
            ('in_progress', 'In Progress'),
            ('solved', 'Solved')
        ],
        default='unsolved'
    )
    


    

    