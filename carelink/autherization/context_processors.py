# from django.shortcuts import render, redirect
# from .forms import FeedbackForm
# from .models import Feedback

# def add_feedback(request):
#     if request.method == 'POST':
#         form = FeedbackForm(request.POST)
#         if form.is_valid():
#             comment = form.cleaned_data['comment']
#             user = request.user
#             feedback = Feedback.objects.create(user=user, comment=comment)
#             feedback.save()
#             return redirect('feedback_success')  # Redirect to a success page
#     else:
#         form = FeedbackForm()

#     return render(request, 'autherization/add_feedback.html', {'form': form})
