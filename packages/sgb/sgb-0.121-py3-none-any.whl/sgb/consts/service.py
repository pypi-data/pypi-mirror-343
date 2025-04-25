import isgb


from sgb.consts.rpc import RPC
from sgb.consts.service_commands import SERVICE_COMMAND
from isgb import SERVICE_ADMIN_HOST_NAME, SERVICE_ADMIN_GRPC_PORT
from sgb.collections.service import ServiceRoleItem, ServiceDescription

EVENT_LISTENER_NAME_PREFIX: str = "_@@EventListener@@_"
SUPPORT_NAME_PREFIX: str = "_@@Support@@_"

SERVICE_DESCRIPTION_HOLDER_VARIABLE_NAME: str = "SD"


class SERVICE_ROLE(ServiceRoleItem):

    SERVICE_ADMIN = ServiceDescription(
        "ServiceAdmin",
        host=SERVICE_ADMIN_HOST_NAME,
        port=RPC.PORT(SERVICE_ADMIN_GRPC_PORT),
        commands=(
            SERVICE_COMMAND.on_service_starts,
            SERVICE_COMMAND.on_service_stops,
            SERVICE_COMMAND.get_service_information_list,
            SERVICE_COMMAND.heart_beat,
        ),
    )

    EVENT = ServiceDescription(
        "Event",
        auto_restart=False,
        commands=(SERVICE_COMMAND.send_log_message, SERVICE_COMMAND.send_event),
    )

    AD = ServiceDescription(
        "ActiveDirectory",
        auto_restart=False,
        commands=(
            SERVICE_COMMAND.get_user_by_full_name,
            SERVICE_COMMAND.get_user_list_by_dn,
            SERVICE_COMMAND.get_template_users,
            SERVICE_COMMAND.get_containers,
            SERVICE_COMMAND.get_user_list_by_job_position,
            SERVICE_COMMAND.get_user_list_by_group,
            SERVICE_COMMAND.get_printer_list,
            SERVICE_COMMAND.create_user_by_template,
            SERVICE_COMMAND.set_user_telephone_number,
            SERVICE_COMMAND.set_user_password,
            SERVICE_COMMAND.set_user_status,
            SERVICE_COMMAND.remove_user,
            SERVICE_COMMAND.drop_user_cache,
            SERVICE_COMMAND.drop_workstaion_cache,
            SERVICE_COMMAND.get_user_list_by_property,
        ),
    )

    SKYPE = ServiceDescription("Skype", auto_restart=False)

    DAMEWARE = ServiceDescription("DameWare", auto_restart=False)

    EXECUTOR = ServiceDescription("Executor", auto_restart=False)

    ROUTER = ServiceDescription("Router", auto_restart=False)
