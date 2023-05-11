import random
import string


def random_generate(size=26, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def generate_slug(model, search_field, length=6):
    """
    generate slug for model.

    :param type model: the model class.
    :param int length: length of generated slug.

    :rtype: str
    """

    generated_slug = random_generate(length)
    filters = {}
    filters[search_field] = generated_slug
    existed = model.objects.filter(**filters).exists()
    if existed is True:
        return generate_slug(model, search_field, length)

    return generated_slug
