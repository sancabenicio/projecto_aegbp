from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from urllib.parse import urlparse, parse_qs
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from googletrans import Translator
from django.db import models
from urllib.parse import urlparse, parse_qs
from django.utils.translation import gettext_lazy as _
from cloudinary.models import CloudinaryField 

translator = Translator()

def translate_fields(instance, fields):
    fields_to_exclude = ['email', 'password', 'username']

    for lang_code, _ in settings.LANGUAGES:
        if lang_code != settings.MODELTRANSLATION_DEFAULT_LANGUAGE:
            for field in fields:
                if field not in fields_to_exclude:
                    value = getattr(instance, field)
                    if value:  # Somente traduzir se o valor não for None ou vazio
                        translated_value = translator.translate(value, dest=lang_code).text
                        setattr(instance, f"{field}_{lang_code}", translated_value)


class Event(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Nome"))
    date = models.DateField(verbose_name=_("Data"))
    description = models.TextField(verbose_name=_("Descrição"))
    start_time = models.TimeField(default=timezone.now, verbose_name=_("Hora de Início"))
    end_time = models.TimeField(default=timezone.now, verbose_name=_("Hora de Término"))

    def save(self, *args, **kwargs):
        if not self.id:
            translate_fields(self, ['name', 'description'])
        else:
            old_instance = Event.objects.get(id=self.id)
            if old_instance.name != self.name or old_instance.description != self.description:
                translate_fields(self, ['name', 'description'])

        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Evento")
        verbose_name_plural = _("Eventos")


class Registration(models.Model):
    event = models.ForeignKey(Event, related_name='registrations', on_delete=models.CASCADE, default=1, verbose_name=_("Evento"))
    name = models.CharField(max_length=100, verbose_name=_("Nome"))
    email = models.EmailField(verbose_name=_("Email"))

    def save(self, *args, **kwargs):
        if not self.id:
            translate_fields(self, ['name'])
        else:
            old_instance = Registration.objects.get(id=self.id)
            if old_instance.name != self.name:
                translate_fields(self, ['name'])

        super(Registration, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.email}"

    class Meta:
        verbose_name = _("Inscrição")
        verbose_name_plural = _("Inscrições")


class Photo(models.Model):
    event = models.ForeignKey(Event, related_name='photos', on_delete=models.CASCADE, verbose_name=_("Evento"))
    image = CloudinaryField(resource_type='image', verbose_name=_("Imagem"))  # Corrigido o uso de CloudinaryField
    caption = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Legenda"))

    def save(self, *args, **kwargs):
        # Tradução da legenda na criação ou atualização
        if not self.id:
            translate_fields(self, ['caption'])
        else:
            old_instance = Photo.objects.get(id=self.id)
            if old_instance.caption != self.caption:
                translate_fields(self, ['caption'])

        # Chamar o método save original
        super(Photo, self).save(*args, **kwargs)

    def __str__(self):
        return self.caption or _("Foto")

    class Meta:
        verbose_name = _("Foto")
        verbose_name_plural = _("Fotos")


class Video(models.Model):
    title = models.CharField(max_length=200, default=_('Título Padrão'), verbose_name=_("Título"))
    description = models.TextField(default=_('Descrição Padrão'), verbose_name=_("Descrição"))
    file = CloudinaryField(resource_type='video', blank=True, null=True, verbose_name=_("Arquivo"))  # Corrigido o uso de CloudinaryField
    link = models.URLField(blank=True, null=True, verbose_name=_("Link Externo"))
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='videos', blank=True, null=True, verbose_name=_("Evento"))

    def save(self, *args, **kwargs):
        # Garantir que os campos de tradução estejam como strings
        self.title = str(self.title)
        self.description = str(self.description)

        # Tradução na criação ou atualização
        if not self.id:
            translate_fields(self, ['title', 'description'])
        else:
            old_instance = Video.objects.get(id=self.id)
            if old_instance.title != self.title or old_instance.description != self.description:
                translate_fields(self, ['title', 'description'])

        # Chamar o método save original
        super(Video, self).save(*args, **kwargs)

    def video_url(self):
        """
        Retorna a URL do arquivo de vídeo, se existir, ou a URL fornecida.
        """
        if self.file:
            return self.file.url  # URL fornecida pelo Cloudinary
        return self.link

    def embed_url(self):
        """
        Retorna a URL embutida do vídeo, se existir. Para vídeos do YouTube,
        transforma a URL em uma URL de embed.
        """
        if self.link:
            return self.get_embed_url()
        return self.video_url()

    def get_embed_url(self):
        """
        Retorna a URL de embed para vídeos do YouTube, se for o caso.
        """
        parsed_url = urlparse(self.link)
        if parsed_url.hostname in ['www.youtube.com', 'youtube.com', 'youtu.be']:
            return self.get_youtube_embed_url(parsed_url)
        return self.link

    def get_youtube_embed_url(self, parsed_url):
        """
        Converte uma URL do YouTube em uma URL de embed.
        """
        if parsed_url.hostname == 'youtu.be':
            video_id = parsed_url.path[1:]
        elif parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
            if parsed_url.path == '/watch':
                video_id = parse_qs(parsed_url.query).get('v', [None])[0]
            elif parsed_url.path.startswith('/embed/') or parsed_url.path.startswith('/v/'):
                video_id = parsed_url.path.split('/')[2]
            else:
                video_id = None
        else:
            video_id = None

        if video_id:
            return f'https://www.youtube.com/embed/{video_id}'
        return self.link

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Vídeo")
        verbose_name_plural = _("Vídeos")


class Document(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Título"))
    file = models.FileField(upload_to='documents/', verbose_name=_("Arquivo"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Descrição"))

    def save(self, *args, **kwargs):
        if not self.id:
            translate_fields(self, ['title', 'description'])
        else:
            old_instance = Document.objects.get(id=self.id)
            if old_instance.title != self.title or old_instance.description != self.description:
                translate_fields(self, ['title', 'description'])

        super(Document, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Documento")
        verbose_name_plural = _("Documentos")


class Sponsor(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Nome"))
    logo = models.ImageField(upload_to='sponsors/', verbose_name=_("Logo"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Descrição"))

    def save(self, *args, **kwargs):
        if not self.id:
            translate_fields(self, ['name', 'description'])
        else:
            old_instance = Sponsor.objects.get(id=self.id)
            if old_instance.name != self.name or old_instance.description != self.description:
                translate_fields(self, ['name', 'description'])

        super(Sponsor, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Patrocinador")
        verbose_name_plural = _("Patrocinadores")


class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Título"))
    content = models.TextField(verbose_name=_("Conteúdo"))
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Autor"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Data de Criação"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Data de Atualização"))
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True, verbose_name=_("Imagem"))

    def save(self, *args, **kwargs):
        if not self.id:
            translate_fields(self, ['title', 'content'])
        else:
            old_instance = BlogPost.objects.get(id=self.id)
            if old_instance.title != self.title or old_instance.content != self.content:
                translate_fields(self, ['title', 'content'])

        super(BlogPost, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Postagem do Blog")
        verbose_name_plural = _("Postagens do Blog")


class Comment(models.Model):
    post = models.ForeignKey(BlogPost, related_name='comments', on_delete=models.CASCADE, verbose_name=_("Postagem"))
    author = models.CharField(max_length=100, verbose_name=_("Autor"))
    content = models.TextField(verbose_name=_("Conteúdo"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Data de Criação"))

    def save(self, *args, **kwargs):
        if not self.id:
            translate_fields(self, ['content'])
        else:
            old_instance = Comment.objects.get(id=self.id)
            if old_instance.content != self.content:
                translate_fields(self, ['content'])

        super(Comment, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.author} em {self.post}'

    class Meta:
        verbose_name = _("Comentário")
        verbose_name_plural = _("Comentários")


class VolunteerOpportunity(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("Título"))
    description = models.TextField(verbose_name=_("Descrição"))
    location = models.CharField(max_length=100, default=_('Desconhecido'), verbose_name=_("Localização"))
    date = models.DateField(verbose_name=_("Data"))

    def save(self, *args, **kwargs):
        self.title = str(self.title)
        self.description = str(self.description)
        self.location = str(self.location)

        if not self.id:
            translate_fields(self, ['title', 'description', 'location'])
        else:
            old_instance = VolunteerOpportunity.objects.get(id=self.id)
            if old_instance.title != self.title or old_instance.description != self.description or old_instance.location != self.location:
                translate_fields(self, ['title', 'description', 'location'])

        super(VolunteerOpportunity, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = _("Oportunidade de Voluntariado")
        verbose_name_plural = _("Oportunidades de Voluntariado")


class Volunteer(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Nome"))
    email = models.EmailField(verbose_name=_("Email"))
    opportunity = models.ForeignKey('VolunteerOpportunity', on_delete=models.CASCADE, verbose_name=_("Oportunidade"))
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Data de Inscrição"))

    def save(self, *args, **kwargs):
        if not self.id:
            translate_fields(self, ['name'])
        else:
            old_instance = Volunteer.objects.get(id=self.id)
            if old_instance.name != self.name:
                translate_fields(self, ['name'])

        super(Volunteer, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Voluntário")
        verbose_name_plural = _("Voluntários")


class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Título"))
    start_date = models.DateField(verbose_name=_("Data de Início"))
    end_date = models.DateField(verbose_name=_("Data de Término"))
    description = models.TextField(verbose_name=_("Descrição"))

    def save(self, *args, **kwargs):
        if not self.id:
            translate_fields(self, ['title', 'description'])
        else:
            old_instance = Project.objects.get(id=self.id)
            if old_instance.title != self.title or old_instance.description != self.description:
                translate_fields(self, ['title', 'description'])

        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Projeto")
        verbose_name_plural = _("Projetos")


class ProjectImpact(models.Model):
    project = models.ForeignKey(Project, related_name='impacts', on_delete=models.CASCADE, verbose_name=_("Projeto"))
    report = models.TextField(verbose_name=_("Relatório"))
    date = models.DateField(verbose_name=_("Data"))

    def save(self, *args, **kwargs):
        if not self.id:
            translate_fields(self, ['report'])
        else:
            old_instance = ProjectImpact.objects.get(id=self.id)
            if old_instance.report != self.report:
                translate_fields(self, ['report'])

        super(ProjectImpact, self).save(*args, **kwargs)

    def __str__(self):
        return f'Relatório de Impacto para {self.project}'

    class Meta:
        verbose_name = _("Impacto do Projeto")
        verbose_name_plural = _("Impactos do Projeto")


class Testimonial(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Nome"))
    content = models.TextField(verbose_name=_("Conteúdo"))
    date = models.DateField(auto_now_add=True, verbose_name=_("Data"))

    def save(self, *args, **kwargs):
        if not self.id:
            translate_fields(self, ['name', 'content'])
        else:
            old_instance = Testimonial.objects.get(id=self.id)
            if old_instance.name != self.name or old_instance.content != self.content:
                translate_fields(self, ['name', 'content'])

        super(Testimonial, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Depoimento")
        verbose_name_plural = _("Depoimentos")


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Nome"))

    def save(self, *args, **kwargs):
        if not self.id:
            translate_fields(self, ['name'])
        else:
            old_instance = Category.objects.get(id=self.id)
            if old_instance.name != self.name:
                translate_fields(self, ['name'])

        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Categoria")
        verbose_name_plural = _("Categorias")


class FAQ(models.Model):
    question = models.CharField(max_length=200, verbose_name=_("Pergunta"))
    answer = models.TextField(verbose_name=_("Resposta"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("Categoria"))

    def save(self, *args, **kwargs):
        if not self.id:
            translate_fields(self, ['question', 'answer'])
        else:
            old_instance = FAQ.objects.get(id=self.id)
            if old_instance.question != self.question or old_instance.answer != self.answer:
                translate_fields(self, ['question', 'answer'])

        super(FAQ, self).save(*args, **kwargs)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = _("Pergunta Frequente")
        verbose_name_plural = _("Perguntas Frequentes")


class ContactMessage(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Nome"))
    email = models.EmailField(verbose_name=_("Email"))
    subject = models.CharField(max_length=255, verbose_name=_("Assunto"))
    message = models.TextField(verbose_name=_("Mensagem"))
    date_sent = models.DateTimeField(auto_now_add=True, verbose_name=_("Data de Envio"))
    status = models.CharField(max_length=50, default='new', verbose_name=_("Status"))
    is_read = models.BooleanField(default=False, verbose_name=_("Lido"))

    def save(self, *args, **kwargs):
        if not self.id:
            translate_fields(self, ['name', 'subject', 'message'])
        else:
            old_instance = ContactMessage.objects.get(id=self.id)
            if old_instance.name != self.name or old_instance.subject != self.subject or old_instance.message != self.message:
                translate_fields(self, ['name', 'subject', 'message'])

        super(ContactMessage, self).save(*args, **kwargs)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = _("Mensagem de Contato")
        verbose_name_plural = _("Mensagens de Contato")



class Message(models.Model):
    contact = models.ForeignKey(ContactMessage, related_name='messages', on_delete=models.CASCADE, verbose_name=_("Contato"))
    sender = models.CharField(max_length=200, verbose_name=_("Remetente"))
    content = models.TextField(verbose_name=_("Conteúdo"))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_("Data/Hora"))

    def save(self, *args, **kwargs):
        # Converta objetos de tradução preguiçosa para strings antes de qualquer operação
        self.sender = str(self.sender)
        self.content = str(self.content)
        
        if not self.id:
            translate_fields(self, ['sender', 'content'])
        else:
            old_instance = Message.objects.get(id=self.id)
            if old_instance.sender != self.sender or old_instance.content != self.content:
                translate_fields(self, ['sender', 'content'])

        super(Message, self).save(*args, **kwargs)

    def __str__(self):
        return f"Mensagem de {self.sender} em {self.timestamp}"

    class Meta:
        verbose_name = _("Mensagem")
        verbose_name_plural = _("Mensagens")



class ContactInfo(models.Model):
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Endereço"))
    phone1 = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Telefone 1"))
    phone2 = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Telefone 2"))
    email1 = models.EmailField(blank=True, null=True, verbose_name=_("Email 1"))
    email2 = models.EmailField(blank=True, null=True, verbose_name=_("Email 2"))
    days_of_week = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Dias da Semana"))
    hours = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Horários"))

    def save(self, *args, **kwargs):
        if not self.id:
            translate_fields(self, ['address', 'phone1', 'phone2', 'days_of_week', 'hours'])
        else:
            old_instance = ContactInfo.objects.get(id=self.id)
            if old_instance.address != self.address or old_instance.phone1 != self.phone1 or old_instance.phone2 != self.phone2 or old_instance.days_of_week != self.days_of_week or old_instance.hours != self.hours:
                translate_fields(self, ['address', 'phone1', 'phone2', 'days_of_week', 'hours'])

        super(ContactInfo, self).save(*args, **kwargs)

    def __str__(self):
        return self.address if self.address else _("Informações de Contato")

    class Meta:
        verbose_name = _("Informação de Contato")
        verbose_name_plural = _("Informações de Contato")


class Donation(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Nome"))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Valor"))
    date = models.DateField(verbose_name=_("Data"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Descrição"))
    proof = models.FileField(upload_to='donation_proofs/', blank=True, null=True, verbose_name=_("Comprovante"))

    def save(self, *args, **kwargs):
        if not self.id:
            translate_fields(self, ['name', 'description'])
        else:
            old_instance = Donation.objects.get(id=self.id)
            if old_instance.name != self.name or old_instance.description != self.description:
                translate_fields(self, ['name', 'description'])

        super(Donation, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - R${self.amount}"

    class Meta:
        verbose_name = _("Doação")
        verbose_name_plural = _("Doações")


class GeneralSettings(models.Model):
    iban = models.CharField(max_length=34, blank=True, null=True, verbose_name=_("IBAN"))
    mb_way_number = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Número MB Way"))

    def save(self, *args, **kwargs):
        if not self.id:
            translate_fields(self, ['iban', 'mb_way_number'])
        else:
            old_instance = GeneralSettings.objects.get(id=self.id)
            if old_instance.iban != self.iban or old_instance.mb_way_number != self.mb_way_number:
                translate_fields(self, ['iban', 'mb_way_number'])

        super(GeneralSettings, self).save(*args, **kwargs)

    def __str__(self):
        return f"IBAN: {self.iban} - MB Way: {self.mb_way_number}"

    class Meta:
        verbose_name = _("Configuração Geral")
        verbose_name_plural = _("Configurações Gerais")


def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 5.0
    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError(f"O tamanho máximo do arquivo é {megabyte_limit}MB")

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("utilizador"))
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, validators=[validate_image], verbose_name=_("Foto de Perfil"))
    job_title = models.CharField(max_length=100, blank=True, default='', verbose_name=_("Cargo"))
    address = models.CharField(max_length=255, blank=True, default='', verbose_name=_("Endereço"))
    city = models.CharField(max_length=100, blank=True, default='', verbose_name=_("Cidade"))
    state = models.CharField(max_length=100, blank=True, default='', verbose_name=_("Estado"))
    zip_code = models.CharField(max_length=10, blank=True, default='', verbose_name=_("CEP"))
    description = models.TextField(blank=True, default='', verbose_name=_("Descrição"))

    def save(self, *args, **kwargs):
        if self.pk is None:
            # Novo objeto
            translate_fields(self, ['job_title', 'address', 'city', 'state', 'zip_code', 'description'])
        else:
            # Atualizar objeto existente
            old_instance = UserProfile.objects.get(pk=self.pk)
            fields_to_translate = []
            for field in ['job_title', 'address', 'city', 'state', 'zip_code', 'description']:
                if getattr(old_instance, field) != getattr(self, field):
                    fields_to_translate.append(field)
            if fields_to_translate:
                translate_fields(self, fields_to_translate)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _("Perfil de utilizador")
        verbose_name_plural = _("Perfis de utilizadores")
        

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class Member(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('CC', _('Cartão de Cidadão')),
        ('PP', _('Passaporte')),
        ('AR', _('Autorização de Residência')),
    ]
    GENDER_CHOICES = [
        ('M', _('Masculino')),
        ('F', _('Feminino')),
        ('O', _('Outro')),
        ('N', _('Prefiro não dizer')),
    ]
    EDUCATION_TYPE_CHOICES = [
        ('S', _('Superior')),
        ('P', _('Profissional')),
        ('T', _('Secundário')),
    ]
    STATUS_CHOICES = [
        ('pending', _('Pendente')),
        ('approved', _('Aprovado')),
        ('rejected', _('Rejeitado')),
    ]

    full_name = models.CharField(max_length=255, verbose_name=_("Nome Completo"))
    birth_date = models.DateField(verbose_name=_("Data de Nascimento"))
    document_number = models.CharField(max_length=100, unique=True, verbose_name=_("Número do Documento"))
    document_type = models.CharField(max_length=2, choices=DOCUMENT_TYPE_CHOICES, verbose_name=_("Tipo de Documento"))
    document_validity = models.DateField(verbose_name=_("Validade do Documento"))
    nationality = models.CharField(max_length=100, verbose_name=_("Nacionalidade"))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name=_("Gênero"))
    other_gender = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Outro Gênero"))
    address = models.CharField(max_length=255, verbose_name=_("Endereço"))
    postal_code = models.CharField(max_length=20, verbose_name=_("Código Postal"))
    city = models.CharField(max_length=100, verbose_name=_("Cidade"))
    phone = models.CharField(max_length=20, verbose_name=_("Telefone"))
    email = models.EmailField(unique=True, verbose_name=_("Email"))
    is_student = models.BooleanField(default=False, verbose_name=_("É Estudante"))
    school = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Escola"))
    education_type = models.CharField(max_length=1, choices=EDUCATION_TYPE_CHOICES, blank=True, null=True, verbose_name=_("Tipo de Educação"))
    course = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Curso"))
    academic_year = models.IntegerField(blank=True, null=True, verbose_name=_("Ano Acadêmico"))
    is_scholar = models.BooleanField(default=False, verbose_name=_("É Bolseiro"))
    is_working_student = models.BooleanField(default=False, verbose_name=_("É Estudante Trabalhador"))
    occupation = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Ocupação"))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name=_("Status"))
    is_read = models.BooleanField(default=False, verbose_name=_("Lido"))

    def save(self, *args, **kwargs):
        if not self.id:
            translate_fields(self, [
                'full_name', 'document_number', 'nationality', 'address',
                'postal_code', 'city', 'phone', 'email', 'school', 
                'course', 'occupation'
            ])
        else:
            old_instance = Member.objects.get(id=self.id)
            fields_to_translate = [
                'full_name', 'document_number', 'nationality', 'address',
                'postal_code', 'city', 'phone', 'email', 'school', 
                'course', 'occupation'
            ]
            for field in fields_to_translate:
                if getattr(old_instance, field) != getattr(self, field):
                    translate_fields(self, [field])

        super(Member, self).save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.gender == 'O' and not self.other_gender:
            raise ValidationError({'other_gender': _('Por favor, especifique o gênero.')})
        if self.birth_date:
            if self.birth_date > timezone.now().date():
                raise ValidationError({'birth_date': _('A data de nascimento não pode ser no futuro.')})
            age = (timezone.now().date() - self.birth_date).days // 365
            if age < 14:
                raise ValidationError({'birth_date': _('A idade do membro deve ser de pelo menos 14 anos.')})
        if self.academic_year is not None and self.academic_year < 1:
            raise ValidationError({'academic_year': _('O ano curricular deve ser maior que zero.')})

    class Meta:
        verbose_name = _("Membro")
        verbose_name_plural = _("Membros")


class PrivacyPolicy(models.Model):
    content = models.TextField(verbose_name=_("Conteúdo"))
    last_updated = models.DateTimeField(auto_now=True, verbose_name=_("Última Atualização"))

    def save(self, *args, **kwargs):
        if not self.id:
            translate_fields(self, ['content'])
        else:
            old_instance = PrivacyPolicy.objects.get(id=self.id)
            if old_instance.content != self.content:
                translate_fields(self, ['content'])

        super(PrivacyPolicy, self).save(*args, **kwargs)

    def __str__(self):
        return f"{_('Política de Privacidade atualizada em')} {self.last_updated}"

    class Meta:
        verbose_name = _("Política de Privacidade")
        verbose_name_plural = _("Políticas de Privacidade")


class About(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Título"))
    description = models.TextField(verbose_name=_("Descrição"))
    image = models.ImageField(upload_to='about_images/', blank=True, null=True, verbose_name=_("Imagem"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Data de Criação"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Data de Atualização"))

    def save(self, *args, **kwargs):
        if not self.id:
            translate_fields(self, ['title', 'description'])
        else:
            old_instance = About.objects.get(id=self.id)
            if old_instance.title != self.title or old_instance.description != self.description:
                translate_fields(self, ['title', 'description'])

        super(About, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Sobre")
        verbose_name_plural = _("Sobre")


class SocialMedia(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', _('Facebook')),
        ('twitter', _('Twitter')),
        ('instagram', _('Instagram')),
        ('linkedin', _('LinkedIn')),
        ('youtube', _('YouTube')),
        ('other', _('Outro')),
    ]

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, verbose_name=_("Plataforma"))
    profile_name = models.CharField(max_length=100, verbose_name=_("Nome do Perfil"))
    url = models.URLField(verbose_name=_("URL"))

    def save(self, *args, **kwargs):
        if not self.id:
            translate_fields(self, ['profile_name'])
        else:
            old_instance = SocialMedia.objects.get(id=self.id)
            if old_instance.profile_name != self.profile_name:
                translate_fields(self, ['profile_name'])

        super(SocialMedia, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_platform_display()} - {self.profile_name}"

    class Meta:
        verbose_name = _("Mídia Social")
        verbose_name_plural = _("Mídias Sociais")
