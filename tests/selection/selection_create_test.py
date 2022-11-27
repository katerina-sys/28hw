import pytest

from tests.factories import AdFactory


@pytest.marko.django_db
def test_selection_create(client, user, ad, access_token):
    ads = AdFactory.create_batch()

    response = client.post('/selection/', {"name": "test selection", "owner": user.pk,
                                           "items": [ad.pk for ad in ads]},
                           HTTP_AUTHORIZATION="Bearer" + access_token)

    assert response.status_code == 201
    assert response.data == {"id": 1, "name": "test selection", "owner": user.pk, "items": [ad.pk for ad in ads]}
