import graphene
from graphene_django import DjangoObjectType
from .models import User as UserModel, App as AppModel

class User(DjangoObjectType):
    class Meta:
        model = UserModel
        fields = ("id", "name", "plan", "apps")

class App(DjangoObjectType):
    class Meta:
        model = AppModel
        fields = ("id", "name", "owner")

class Query(graphene.ObjectType):
    all_users = graphene.List(User)
    all_apps = graphene.List(App)
    user = graphene.Field(User, id=graphene.ID(required=True))
    app = graphene.Field(App, id=graphene.ID(required=True))

    def resolve_all_users(self, info):
        return UserModel.objects.all()

    def resolve_all_apps(self, info):
        return AppModel.objects.all()

    def resolve_user(self, info, id):
        return UserModel.objects.get(pk=id)

    def resolve_app(self, info, id):
        return AppModel.objects.get(pk=id)

class CreateUser(graphene.Mutation):
    user = graphene.Field(User)
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        plan = graphene.String(required=True)
    def mutate(self, info, name, email, plan):
        return CreateUser(user=UserModel.objects.create(name=name, email=email, plan=plan))

class CreateApp(graphene.Mutation):
    app = graphene.Field(App)
    class Arguments:
        name = graphene.String(required=True)
        owner_id = graphene.ID(required=True)
    def mutate(self, info, name, owner_id):
        owner = UserModel.objects.get(pk=owner_id)
        return CreateApp(app=AppModel.objects.create(name=name, owner=owner))

class UpgradeAccount(graphene.Mutation):
    user = graphene.Field(User)
    class Arguments:
        user_id = graphene.ID(required=True)
    def mutate(self, info, user_id):
        user = UserModel.objects.get(pk=user_id)
        user.plan = "PRO"
        user.save()
        return UpgradeAccount(user=user)

class DowngradeAccount(graphene.Mutation):
    user = graphene.Field(User)
    class Arguments:
        user_id = graphene.ID(required=True)
    def mutate(self, info, user_id):
        user = UserModel.objects.get(pk=user_id)
        user.plan = "HOBBY"
        user.save()
        return DowngradeAccount(user=user)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_app = CreateApp.Field()
    upgrade_account = UpgradeAccount.Field()
    downgrade_account = DowngradeAccount.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
