from datetime import datetime
from contact_persons_local.contact_persons_local import ContactPersonsLocal
from database_mysql_local.generic_mapping import GenericMapping
from language_remote.lang_code import LangCode
from logger_local.MetaLogger import MetaLogger
from profile_local.profiles_local import ProfilesLocal
from user_context_remote.user_context import UserContext

from .contact_profiles_local_constants import (
    CONTACT_PROFILES_PYTHON_PACKAGE_CODE_LOGGER_OBJECT,
)

CONTACT_PROFILE_SCHEMA_NAME = "contact_profile"
CONTACT_ENTITY_NAME = "contact"
PROFILE_ENTITY_NAME = "profile"
CONTACT_PROFILE_ID_COLUMN_NAME = "contact_profile_id"
CONTACT_PROFILE_TABLE_NAME = "contact_profile_table"
CONTACT_PROFILE_VIEW_NAME = "contact_profile_view"
LINKEDIN_DATA_SOURCE_TYPE_ID = 18
RISHON_MUNI_EXHIBITOR_CSV_DATA_SOURCE_TYPE_ID = 60

user_context = UserContext()


class ContactProfilesLocal(
    GenericMapping,
    metaclass=MetaLogger,
    object=CONTACT_PROFILES_PYTHON_PACKAGE_CODE_LOGGER_OBJECT,
):
    """Class to manage many ContactProfile Objects."""

    def __init__(self, lang_code: LangCode = None, is_test_data: bool = False) -> None:

        GenericMapping.__init__(
            self,
            default_schema_name=CONTACT_PROFILE_SCHEMA_NAME,
            default_entity_name1=CONTACT_ENTITY_NAME,
            default_entity_name2=PROFILE_ENTITY_NAME,
            default_column_name=CONTACT_PROFILE_ID_COLUMN_NAME,
            default_table_name=CONTACT_PROFILE_TABLE_NAME,
            default_view_table_name=CONTACT_PROFILE_VIEW_NAME,
            is_test_data=is_test_data,
        )
        self.profiles_local = ProfilesLocal(is_test_data=is_test_data)
        self.contact_persons_local = ContactPersonsLocal(is_test_data=is_test_data)
        # TODO: I think we can delete the following line and lang_code parameter
        self.lang_code = (
            lang_code or user_context.get_effective_profile_preferred_lang_code()
        )

    def insert_and_link_contact_profile(
        self,
        *,
        contact_dict: dict,
        contact_id: int = None,
        person_id: int = None,
        visibility_id: int = 0,
        is_approved: bool = True,
        stars: int = 0,
        last_dialog_workflow_state_id: int = 1
    ) -> dict:
        """Insert contact and link to existing or new email address"""
        self.logger.start(
            "insert_and_link_contact_profile",
            object={
                "contact_dict": contact_dict,
                "contact_id": contact_id,
                "person_id": person_id,
                "visibility_id": visibility_id,
                "is_approved": is_approved,
                "stars": stars,
                "last_dialog_workflow_state_id": last_dialog_workflow_state_id,
            },
        )
        # We prefer to get contact_id from contact_dict, but for backward compatibility we also accept contact_id argument
        contact_id = contact_dict.get("contact_id") or contact_id
        # We prefer to get person_id from contact_dict, but for backward compatibility we also accept person_id argument
        person_id = contact_dict.get("person_id") or person_id
        person_ids_list = self.contact_persons_local.get_person_ids_by_contact_id(
            contact_id=contact_id, limit=1, order_by="contact_person_id DESC"
        )
        profiles_ids_list = []
        contact_profiles_ids_list = []
        if person_id is not None and person_id not in person_ids_list:
            self.logger.info(
                "insert_and_link_contact_profile: person_id is not in person_ids, adding it to person_ids",
                object={"person_id": person_id, "person_ids_list": person_ids_list},
            )
            person_ids_list.insert(0, person_id)
        if person_ids_list:
            person_id = person_ids_list[0]
            self.logger.info(
                "insert_and_link_contact_profile: person_id is set to the first element of person_ids_list",
                object={"person_id": person_id, "person_ids_list": person_ids_list},
            )
            # TODO profile_ids_of_a_person_tuple_list
            profile_ids_tuples_list = (
                self.profiles_local.select_multi_tuple_by_column_and_value(
                    select_clause_value="profile_id",
                    column_name="main_person_id",
                    column_value=person_id,
                )
            )
            self.logger.info(
                "insert_and_link_contact_profile: profile_ids_tuples_list",
                object={"profile_ids_tuples_list": profile_ids_tuples_list},
            )
            if not profile_ids_tuples_list:
                # Create a new  profile and add it to profile_table and profile_ml_table
                self.logger.info(
                    "profile_id is None, creating a new profile and adding it to"
                    " profile_table and profile_ml_table"
                )
                lang_code_str = LangCode.detect_lang_code_str_restricted(
                    text=contact_dict.get("display_as"),
                    default_lang_code=LangCode.ENGLISH.value,
                )
                profile_dict = {
                    "main_person_id": person_id,
                    "profile.name": contact_dict.get("display_as"),
                    "lang_code": lang_code_str,
                    "visibility_id": visibility_id,
                    "is_approved": is_approved,
                    "is_main": True,
                    "stars": stars,
                    "last_dialog_workflow_state_id_old": last_dialog_workflow_state_id,
                }
                profile_id = self.profiles_local.insert(
                    main_person_id=person_id, profile_dict=profile_dict
                )
                if profile_id is None:
                    self.logger.error(
                        "profile was not created and inserted to the database, profile_id is None",
                        object={
                            "contact_id": contact_id,
                            "profile_id": profile_id,
                            "person_id": person_id,
                        },
                    )
                    self.logger.end("insert_and_link_contact_profile")
                    return {}
                else:
                    contact_dict["created_for_contact_profile_id"] = profile_id
                    self.logger.info(
                        "profile was created and inserted to the database",
                        object={"profile_id": profile_id},
                    )
                    profiles_ids_list.append(profile_id)

                self.logger.info(
                    "profile was created and inserted to the database",
                    object={"profile_id": profile_id},
                )
                self.logger.info(
                    "Linking contact to profile",
                    object={"contact_id": contact_id, "profile_id": profile_id},
                )
                contact_profile_id = self.insert_mapping(
                    entity_name1=self.default_entity_name1,
                    entity_name2=self.default_entity_name2,
                    entity_id1=contact_id,
                    entity_id2=profile_id,
                )
                if contact_profile_id is None:
                    self.logger.error(
                        "contact was not linked to profile, contact_profile_id is None",
                        object={"contact_id": contact_id, "profile_id": profile_id},
                    )
                    self.logger.end("insert_and_link_contact_profile")
                    return {}
                self.logger.info(
                    "contact was linked to profile",
                    object={"contact_id": contact_id, "profile_id": profile_id},
                )
                contact_profiles_ids_list.append(contact_profile_id)
                # Update main_profile_id in contact_table and person_table
                self.update_by_column_and_value(
                    schema_name="contact",
                    table_name="contact_table",
                    column_name="contact_id",
                    column_value=contact_id,
                    data_dict={"main_profile_id": profile_id},
                )
                contact_dict["main_profile_id"] = profile_id
                self.__link_job_title_profile(
                    contact_dict=contact_dict, profile_id=profile_id
                )
                self.update_by_column_and_value(
                    schema_name="person",
                    table_name="person_table",
                    column_name="person_id",
                    column_value=person_id,
                    data_dict={"person.main_profile_id": profile_id},
                )
                self.set_schema(schema_name="contact_profile")
            else:
                for profile_id_tuple in profile_ids_tuples_list:
                    # Check if there is link to existing profile
                    self.logger.info(
                        "Checking if there is link to existing profile",
                        object={
                            "contact_id": contact_id,
                            "profile_id": profile_id_tuple[0],
                        },
                    )
                    profile_id = profile_id_tuple[0]
                    mapping_tuple_list = self.select_multi_mapping_tuple_by_id(
                        entity_name1=self.default_entity_name1,
                        entity_name2=self.default_entity_name2,
                        entity_id1=contact_id,
                        entity_id2=profile_id,
                    )
                    if not mapping_tuple_list:
                        # Link contact to existing profile
                        self.logger.info(
                            "Linking contact to existing profile",
                            object={"contact_id": contact_id, "profile_id": profile_id},
                        )
                        contact_profile_id = self.insert_mapping(
                            entity_name1=self.default_entity_name1,
                            entity_name2=self.default_entity_name2,
                            entity_id1=contact_id,
                            entity_id2=profile_id,
                        )
                    else:
                        self.logger.info(
                            "contact is already linked to profile",
                            object={"contact_id": contact_id, "profile_id": profile_id},
                        )
                        contact_profile_id = mapping_tuple_list[0][0]

                    profiles_ids_list.append(profile_id)
                    contact_profiles_ids_list.append(contact_profile_id)
                    if len(profile_ids_tuples_list) == 1:
                        self.__link_job_title_profile(
                            contact_dict=contact_dict, profile_id=profile_id
                        )
            profile_profile_ids_list = self.__insert_profile_profile_mappings(
                profile_ids=profiles_ids_list, contact_dict=contact_dict
            )
            insert_information = {
                "contact_profiles_ids_list": contact_profiles_ids_list,
                "contact_id": contact_id,
                "profiles_ids_list": profiles_ids_list,
                "profile_profile_ids_list": profile_profile_ids_list,
            }
            self.logger.end(
                "insert_and_link_contact_profile",
                object={"insert_information": insert_information},
            )
            return insert_information

    # TODO Shall we move it to a separate file? separate repo?
    # TODO Shall we use the existing naming convention like PersonProfilesLocal.link_person_id_profile_id(...)?
    def __insert_profile_profile_mappings(
        self, *, profile_ids: list[int], contact_dict: dict
    ) -> list[int]:
        """Insert profile_profile mappings"""
        self.logger.start(
            "__insert_profile_profile_mappings",
            object={"profile_ids": profile_ids, "contact_dict": contact_dict},
        )
        owner_profile_id = contact_dict.get("owner_profile_id")
        if not owner_profile_id:
            return None
        profile_profile_mappings_ids_list = []
        for profile_id in profile_ids:
            if profile_id == owner_profile_id:
                continue
            added_timestamp = contact_dict.get("added_timestamp")
            if (
                added_timestamp
                and contact_dict.get("data_source_type_id")
                == LINKEDIN_DATA_SOURCE_TYPE_ID
            ):
                # Convert timestamp from the format "25 Aug 2023" to the format '2023-08-25 00:00:00'
                datetime_obj = datetime.strptime(added_timestamp, "%d %b %Y")
                formatted_added_timestamp = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
            elif (
                added_timestamp
                and contact_dict.get("data_source_type_id")
                == RISHON_MUNI_EXHIBITOR_CSV_DATA_SOURCE_TYPE_ID
            ):
                # Convert timestamp from the format "09 June 2024, 16:29:15" to the format '2024-06-09 16:29:15'
                datetime_obj = datetime.strptime(added_timestamp, "%d %B %Y, %H:%M:%S")
                formatted_added_timestamp = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
            else:
                formatted_added_timestamp = None
            data_dict = {
                "profile_id1": owner_profile_id,
                "profile_id2": profile_id,
                "relationship_type_id": 1,  # TODO: What is this?
                "start_timestamp": formatted_added_timestamp,
                "system_id": contact_dict.get("system_id"),
            }
            data_dict_compare = {
                "profile_id1": owner_profile_id,
                "profile_id2": profile_id,
                "relationship_type_id": 1,  # TODO: What is this?
                "system_id": contact_dict.get("system_id"),
            }
            profile_profile_mapping_id = self.upsert(
                schema_name="profile_profile",
                data_dict=data_dict,
                table_name="profile_profile_table",
                view_table_name="profile_profile_view",
                data_dict_compare=data_dict_compare,
            )
            self.set_schema(schema_name="contact_profile")
            profile_profile_mappings_ids_list.append(profile_profile_mapping_id)
        self.logger.end(
            "__insert_profile_profile_mappings",
            object={
                "profile_profile_mappings_ids_list": profile_profile_mappings_ids_list
            },
        )
        return profile_profile_mappings_ids_list

    def __link_job_title_profile(self, *, contact_dict: dict, profile_id: int) -> None:
        """Link job title to profile"""
        self.logger.start(
            "__link_job_title_profile",
            object={"contact_dict": contact_dict, "profile_id": profile_id},
        )
        linked_group_results_list = contact_dict.get("linked_group_results_list")
        if not linked_group_results_list:
            return
        for index, linked_group_results in enumerate(linked_group_results_list):
            job_title_id = linked_group_results.get("job_title_id")
            job_title_ml_id = linked_group_results.get("job_title_ml_id")
            if job_title_id is not None:
                data_dict_compare = {
                    "profile_id": profile_id,
                    "job_title_id": job_title_id,
                    "job_title_ml_id": job_title_ml_id,
                }
                job_title_profile_id_list = (
                    self.insert_mapping_if_not_exists_with_ml_ids(
                        schema_name="job_title_profile",
                        entity_name1="job_title",
                        entity_name2="profile",
                        entity_id1=job_title_id,
                        entity_id2=profile_id,
                        entity_ml_ids_list1=[job_title_ml_id],
                        view_table_name="job_title_profile_view",
                        data_dict_compare=data_dict_compare,
                    )
                )
                job_title_profile_id = (
                    job_title_profile_id_list[0] if job_title_profile_id_list else None
                )
                contact_dict["linked_group_results_list"][index][
                    "job_title_profile_id"
                ] = job_title_profile_id
