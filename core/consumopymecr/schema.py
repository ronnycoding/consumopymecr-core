import graphene
import graphql_jwt
from users.models import CustomUser
from graphene_django import DjangoObjectType
import graphene

class User(DjangoObjectType):
    class Meta:
        model = CustomUser

class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

class Query(graphene.ObjectType):
    viewer = graphene.Field(User)
    users = graphene.List(User)

    def resolve_viewer(self, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception('Authentication credentials were not provided')
        return user

    def resolve_users(self, info):
        return CustomUser.objects.all()

schema = graphene.Schema(mutation=Mutation, query=Query)