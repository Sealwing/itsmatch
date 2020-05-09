from django.utils.datastructures import MultiValueDict
from django.http.request import QueryDict
from django.core.paginator import Paginator, InvalidPage
from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings
from django.urls import reverse

from .models import Human

HUMANS_CREATE_REQUIRED_FIELDS = {'age', 'gender', 'first_name', 'second_name'}


def humans_get_all(params) -> tuple:
    """
    TODO docstring
    """
    humans = Human.objects.all()
    if len(humans) == 0:
        return (204, {'description': 'No objects found.'}, None)
    paginator = Paginator(humans, settings.PAGINATION_CONSTS['HUMAN'])
    page_number = params['page'] if 'page' in params else 1
    try:
        page_data = paginator.page(page_number)
        links = [
            {'first': f"{reverse('humans')}?page=1"}
            if paginator.num_pages > 1 else None,
            {'last': f"{reverse('humans')}?page={paginator.num_pages}"}
            if paginator.num_pages > 1 else None,
            {'prev': f"{reverse('humans')}?page={page_data.previous_page_number()}"}
            if page_data.has_previous() else None,
            {'next': f"{reverse('humans')}?page={page_data.next_page_number()}"}
            if page_data.has_next() else None,
            {'self': f"{reverse('humans')}?page={page_number}"}
            if paginator.num_pages > 1 else None,
        ]
        links = [x for x in links if x is not None]
        return (200,
                {'objects': [str(record) for record in page_data]},
                links)
    except InvalidPage:
        return (404, {'description': 'Wrong page provided.'}, None)


def humans_create(params: QueryDict, files: MultiValueDict) -> tuple:
    """
    TODO docstring
    """
    # check params (all have to be present)
    if len(HUMANS_CREATE_REQUIRED_FIELDS - set(params.keys())) != 0:
        params_not_presented: str = ', '.join(HUMANS_CREATE_REQUIRED_FIELDS - set(params.keys()))
        return (400, {
            'description': f'Some of required parameters was not provided. Lost parameters: {params_not_presented}'
        })

    # check avatar on None to use default picture
    avatar, avatar_load_description = __detect_avatar_to_provide__(files)

    # try to create entry in database
    try:
        new_entry = Human(first_name=params['first_name'], second_name=params['second_name'],
                          age=params['age'], gender=params['gender'], avatar=avatar)
        new_entry.save()
        return (201, {'description': 'Human successfully created.'})
    except Exception as e:
        print(e)
        # TODO remove it in production only for debugging
        if settings.DEBUG:
            return (500, {'description': f'{e}'})
        else:
            return (500, {'description': ''})


def __detect_avatar_to_provide__(files: MultiValueDict) -> tuple:
    # Можно вынести нейминг параметров в отдельный файл, чтобы рефакторить было более реально
    if 'avatar' in files.keys():
        avatar = files['avatar']
        return avatar, ''
    else:
        return None, 'A picture could be passed to be used as human avatar.'


def humans_get_details(id) -> tuple:
    try:
        human = Human.objects.get(pk=id)
        result = {
            'first_name': human.first_name,
            'second_name': human.second_name,
            'gender': human.get_gender_str(),
            'age': human.age,
            # for test
            'avatar': human.avatar.name,
        }
        return (200, result)
    except ObjectDoesNotExist:
        return (404, {'description': 'No human with such id.'})


def humans_update_details(id, params) -> tuple:
    try:
        human = Human.objects.get(pk=id)
        try:
            for field in HUMANS_CREATE_REQUIRED_FIELDS.intersection(set(params.keys())):
                # Здесь можно нарастить try-except для более детализированного ответа о падении
                setattr(human, field, params[field])
            human.save()
            return (200, {'description': f'Entry {human} was successfully updated.'})
        except Exception as e:
            print(e)
            return (400, {'description': 'Can not assign passed values.'})
    except ObjectDoesNotExist:
        return (404, {'description': 'No human with such id.'})


def humans_delete_details(id) -> tuple:
    try:
        human = Human.objects.get(pk=id)
        human.delete()
        return (204, {'description': f'Human {human} was deleted.'})
    except ObjectDoesNotExist:
        return (404, {'description': 'No human with such id'})
