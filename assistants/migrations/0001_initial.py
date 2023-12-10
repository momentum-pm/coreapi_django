# Generated by Django 4.2.7 on 2023-12-10 11:10

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import utils.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assistant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remote_uuid', models.TextField()),
                ('name', models.CharField(max_length=255)),
                ('instructions', models.TextField()),
                ('files', models.ManyToManyField(blank=True, to='files.file')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', utils.models.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', utils.models.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='GoalDefinerAssistant',
            fields=[
                ('assistant_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='assistants.assistant')),
            ],
            options={
                'abstract': False,
            },
            bases=('assistants.assistant',),
            managers=[
                ('objects', utils.models.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remote_uuid', models.TextField()),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='threads', to='assistants.member')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', utils.models.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Run',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('remote_uuid', models.TextField()),
                ('state', models.CharField(default='queued', max_length=20)),
                ('instructions', models.TextField()),
                ('assistant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='runs', to='assistants.assistant')),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='runs', to='assistants.thread')),
            ],
            options={
                'ordering': ['-created_at'],
            },
            managers=[
                ('objects', utils.models.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('is_response', models.BooleanField(default=False)),
                ('remote_uuid', models.TextField()),
                ('content', models.TextField()),
                ('files', models.ManyToManyField(blank=True, to='files.file')),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='assistants.thread')),
            ],
            options={
                'ordering': ['-created_at'],
            },
            managers=[
                ('objects', utils.models.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Function',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specification', models.JSONField()),
                ('assistant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='functions', to='assistants.assistant')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', utils.models.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='assistant',
            name='member',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='assistant', to='assistants.member'),
        ),
    ]
