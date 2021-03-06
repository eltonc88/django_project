from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render

from .forms import ContactForm, SignUpForm
from .models import SignUp

# Create your views here.
def home(request):
    title = 'Sign Up Now ' # if request.user.is_authenticated():
    #     title = "My Title %s" %(request.user)
    # if request.method == "POST":
    #     print request.POST
    form = SignUpForm(request.POST or None)
    context = {
        "template_title": title,
        "form": form,
    }

    if form.is_valid():
        # form.save()
        instance = form.save(commit=False)
        print request.POST['email']
        full_name = form.cleaned_data.get("full_name")
        if not full_name:
            full_name = "New full name"
        instance.full_name = full_name
        # if not instance.full_name == None:
        #     instance.full_name = "Justin"
        instance.save()
        context = {
            "title": "Thank you"
        }

    if request.user.is_authenticated() and request.user.is_staff:
        # print(SignUp.objects.all())
        # i = 1
        # for instance in SignUp.objects.all():
        #     print(i)
        #     print(instance.full_name)
        #     i += 1
        queryset = SignUp.objects.all().order_by('-timestamp')
        # queryset = SignUp.objects.all().order_by('-timestamp').filter(full_name__icontains="justin")
        # queryset = SignUp.objects.all().order_by('-timestamp').filter(full_name__iexact="justin")
        # queryset = SignUp.objects.all().order_by('-timestamp').filter(full_name__iexact="justin").count
        print(SignUp.objects.all().order_by('-timestamp').filter(full_name__iexact="justin").count)

        context = {
            "queryset": queryset,
        }

    return render(request, "home.html", context)

def contact(request):
    title = "Contact Us"
    title_align_center = True
    form = ContactForm(request.POST or None)

    if form.is_valid():
        # for key, value in form.cleaned_data.iteritems():
            # print key, value
            # print form.cleaned_data.get(key)
        form_email = form.cleaned_data.get("email")
        form_message = form.cleaned_data.get("message")
        form_full_name = form.cleaned_data.get("full_name")
        # print email, message, full_name
        subject = 'Site Contact Form'
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email, 'otherEmail@gmail.com']
        contact_message = "%s: %s via %s"%(
            form_full_name,
            form_message,
            form_email)
        html_message = """
            <h1>message from %s</h1>
            <p>%s</p>
            <p>email contact: %s</p>"""%(
            form_full_name,
            form_message,
            form_email)

        send_mail(subject,
            contact_message,
            form_email,
            to_email,
            html_message=some_html_message,
            fail_silently=False)

    context = {
        "form": form,
        "title": title,
        "title_align_center": title_align_center,
    }

    return render(request, "forms.html", context)
