# VPN Service

## Description

A web program that executes proxy requests

![image](https://github.com/Moryee/vpn-service/assets/82435275/63c15c9e-a103-448e-ae7c-29534d6f2745)

## How to run
- Run project with docker compose `docker-compose up -d --build`
- You need to make manual migrations inside backend container 

`docker-compose exec backend python manage.py makemigrations --noinput`

`docker-compose exec backend python manage.py migrate --noinput`

- Program will be available on http://localhost:8000/
- To stop program and delete docker containers

`docker-compose down -v`

## Technical details

Program done with: Django, PostgreSQL, Docker

### Site model and views details

- Site model
```py
class Site(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    visiting_count = models.BigIntegerField(default=0)
    data_volume = models.BigIntegerField(default=0)
```

- Sites have CRUD operations as you can see in the screenshot, all of them require login, some of them require owner permission
```py
class SiteListView(LoginRequiredMixin, View):
class SiteDetailView(LoginRequiredMixin, View):
class SiteCreateView(LoginRequiredMixin, View):
class SiteUpdateView(LoginRequiredMixin, View):
class SiteDeleteView(LoginRequiredMixin, DeleteView):
```

### VPN
- Proxy require login because it records statistics on visits

```py
app/proxy/views.py 12
class ProxyIndexView(LoginRequiredMixin, View):
```

- Get request requires url for the request and a pk to to know if the user is the owner of the created site

```py
app/proxy/views.py 14
    ...
        url = request.GET.get('url', '')
        if not url:
            return HttpResponse('No url specified', status=400)
        pk = request.GET.get('pk', '')
        if not pk:
            return HttpResponse('No pk specified', status=400)
        site = Site.objects.get(pk=pk)
        if request.user != site.user:
            return HttpResponse('You are not owner of this site', status=400)
    ...
```

- Then the program copies request data and makes a request
- Replaces all necessary links, collects statistics, generates response and sends it back
```py
app/proxy/views.py 53
    ...
        def replace_url(match):
            matched_url = match.group(1)

            matched_url_netloc = urlparse(matched_url).netloc
            if matched_url_netloc == urlparse(url).netloc:
                matched_url = '/'.join(matched_url.split('//')[1].split('/')[1:])
            elif matched_url_netloc:
                return f'href="{matched_url}"'

            matched_url = urljoin(url, matched_url)
            replacement_url = f'href="{view_link}?url={matched_url}&pk={pk}"'
            return replacement_url

        modified_content = re.sub(r'href="([^"]+)"', replace_url, modified_content.decode('utf-8', errors='ignore')).encode('utf-8')
    ...
        site.visiting_count += 1
        site.data_volume += len(modified_content) + len(request.body)
    ...
```
