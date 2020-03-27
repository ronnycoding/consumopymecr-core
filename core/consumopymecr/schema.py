import graphene
import graphql_jwt
from users.models import CustomUser
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import superuser_required, login_required

class User(DjangoObjectType):
    class Meta:
        model = CustomUser

class Mutation(graphene.ObjectType):
    # user = graphene.Field(User, id=graphene.Int())
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    # delete_token_cookie = graphql_jwt.relay.DeleteJSONWebTokenCookie.Field()

    # Long running refresh tokens
    revoke_token = graphql_jwt.relay.Revoke.Field()

    # delete_refresh_token_cookie = \
    #     graphql_jwt.refresh_token.relay.DeleteRefreshTokenCookie.Field()

    def resolve_user(self, info, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')
        user = CustomUser(email=email)
        user.set_password(raw_password=password)
        user.save()

        if user.id is not None:
            return User.objects.get(pk=user.id)

        return None

class Query(graphene.ObjectType):
    viewer = graphene.Field(User, token=graphene.String(required=True))
    users = graphene.List(User)

    @login_required
    def resolve_viewer(self, info, **kwargs):
        return info.context.user
        # user = info.context.user
        # if not user.is_authenticated:
        #     raise Exception('Authentication credentials were not provided')
        # return user

    @superuser_required
    def resolve_users(self, info):
        return CustomUser.objects.all()

schema = graphene.Schema(mutation=Mutation, query=Query)