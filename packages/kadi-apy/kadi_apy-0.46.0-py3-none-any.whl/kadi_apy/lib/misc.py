# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from kadi_apy.lib.commons import RequestMixin
from kadi_apy.lib.commons import VerboseMixin
from kadi_apy.lib.imports import import_eln
from kadi_apy.lib.imports import import_json_schema
from kadi_apy.lib.imports import import_shacl
from kadi_apy.lib.utils import _get_record_identifiers
from kadi_apy.lib.utils import append_identifier_suffix
from kadi_apy.lib.utils import get_resource_type
from kadi_apy.lib.utils import paginate


class Miscellaneous(RequestMixin, VerboseMixin):
    """Model to handle miscellaneous functionality.

    :param manager: Manager to use for all API requests.
    :type manager: KadiManager
    """

    def get_deleted_resources(self, **params):
        r"""Get a list of deleted resources in the trash. Supports pagination.

        :param \**params: Additional query parameters.
        :return: The response object.
        """

        endpoint = "/trash"
        return self._get(endpoint, params=params)

    def restore(self, item, item_id):
        """Restore an item from the trash.

        :param item: The resource type defined either as string or class.
        :param item_id: The ID of the item to restore.
        :type item_id: int
        :return: The response object.
        """

        if isinstance(item, str):
            item = get_resource_type(item)

        endpoint = f"{item.base_path}/{item_id}/restore"
        return self._post(endpoint)

    def purge(self, item, item_id):
        """Purge an item from the trash.

        :param item: The resource type defined either as string or class.
        :param item_id: The ID of the item to restore.
        :type item_id: int
        :return: The response object.
        """

        if isinstance(item, str):
            item = get_resource_type(item)

        endpoint = f"{item.base_path}/{item_id}/purge"
        return self._post(endpoint)

    def get_licenses(self, **params):
        r"""Get a list of available licenses.  Supports pagination.

        :param \**params: Additional query parameters.
        :return: The response object.
        """

        endpoint = "/licenses"
        return self._get(endpoint, params=params)

    def get_kadi_info(self):
        """Get information about the Kadi instance.

        :return: The response object.
        """

        endpoint = "/info"
        return self._get(endpoint)

    def get_roles(self):
        """Get all possible roles and corresponding permissions of all resources.

        :return: The response object.
        """

        endpoint = "/roles"
        return self._get(endpoint)

    def get_tags(self, **params):
        r"""Get a list of all tags. Supports pagination.

        :param \**params: Additional query parameters.
        :return: The response object.
        """

        endpoint = "/tags"
        return self._get(endpoint, params=params)

    def import_eln(self, file_path):
        """Import an RO-Crate file following the "ELN" file specification.

        :param file_path: The path of the file.
        :type file_path: str
        :raises KadiAPYInputError: If the structure of the RO-Crate is not valid.
        :raises KadiAPYRequestError: If any request was not successful while importing
            the data and metadata.
        """
        import_eln(self.manager, file_path)

    def import_json_schema(self, file_path, template_type="extras"):
        """Import JSON Schema file and create a template.

        Note that only JSON Schema draft 2020-12 is fully supported, but older schemas
        might still work.

        :param file_path: The path of the file.
        :type file_path: str
        :param template_type: Type of the template. Can either be ``"record"`` or
            ``"extras"``.
        :type template_type: str
        :raises KadiAPYInputError: If the structure of the Schema is not valid.
        :raises KadiAPYRequestError: If any request was not successful while importing
            the metadata.
        """
        import_json_schema(self.manager, file_path, template_type)

    def import_shacl(self, file_path, template_type="extras"):
        """Import SHACL Shapes file and create a template.

        :param file_path: The path of the file.
        :type file_path: str
        :param template_type: Type of the template. Can either be ``"record"`` or
            ``"extras"``.
        :type template_type: str
        :raises KadiAPYInputError: If the structure of the Shapes is not valid.
        :raises KadiAPYRequestError: If any request was not successful while importing
            the metadata.
        """
        import_shacl(self.manager, file_path, template_type)

    def reuse_collection(self, collection_id, suffix):
        """Reuse the collection with the given ID.

        This method creates a new collection by duplicating all records from an existing
        collection and appending the given suffix to their identifiers. It ensures that
        record links are preserved within the modified collection. Note that currently
        only the metadata of records is copied.

        :param collection_id: The ID of the collection to be reused.
        :param suffix: A string to append to each record and collection identifier.
        :raises KadiAPYRequestError: If any request was not successful during the
            duplication process.
        """
        collection = self.manager.collection(id=collection_id)

        new_identifier = append_identifier_suffix(collection.meta["identifier"], suffix)
        new_collection = self.manager.collection(
            title=collection.meta["title"],
            identifier=new_identifier,
            description=collection.meta["description"],
            tags=collection.meta["tags"],
            visibility=collection.meta["visibility"],
            create=True,
        )

        record_identifiers = _get_record_identifiers(collection)
        _copy_records(self.manager, new_collection, record_identifiers, suffix)

        # Link the new collection as a child to the existing collection.
        collection.add_collection_link(collection_id=new_collection.id)


def _copy_records(manager, collection, record_identifiers, suffix):
    records = {}

    for identifier in record_identifiers:
        record = manager.record(identifier=identifier)

        new_identifier = append_identifier_suffix(identifier, suffix)
        new_record = manager.record(
            title=record.meta["title"],
            identifier=new_identifier,
            type=record.meta["type"],
            description=record.meta["description"],
            extras=record.meta["extras"],
            tags=record.meta["tags"],
            visibility=record.meta["visibility"],
            license=record.meta["license"],
            create=True,
        )

        records[identifier] = {
            "old_record": record,
            "new_record": new_record,
        }

        # Add the new record to the new collection.
        collection.add_record_link(record_id=new_record.id)

    # Process links only after all records are created.
    for record_data in records.values():
        old_record = record_data["old_record"]
        new_record = record_data["new_record"]

        def _process_record_links(page, old_record=old_record, new_record=new_record):
            response = old_record.get_record_links(
                direction="out", per_page=100, page=page
            ).json()

            for link in response["items"]:
                record_to_identifier = link["record_to"]["identifier"]

                if record_to_identifier in records:
                    new_record_to = records[record_to_identifier]["new_record"]
                    new_record.link_record(
                        record_to=new_record_to.id, name=link["name"]
                    )

            return response

        paginate(_process_record_links)
