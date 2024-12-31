/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { FileType } from './FileType';
/**
 * File model for storing file metadata and references
 *
 * Attributes:
 * documentation_type (DocumentationType): Type of documentation (e.g., REPAIR_MANUAL)
 * title (str): Title of the documentation
 * filename (str): filename of the file (e.g., S3 object name)
 * description (Optional[str]): Optional detailed description of the document
 */
export type File = {
    /**
     * Document ID
     */
    _id: string;
    /**
     * File type
     */
    type?: FileType;
    /**
     * File title
     */
    title: string;
    /**
     * File name, like an S3 object name
     */
    internal_filename: string;
    /**
     * File description
     */
    description: (string | null);
    /**
     * Owner of the file
     */
    owner_user_id: string;
    /**
     * Entity that the file is associated with
     */
    entity_id: string;
    /**
     * Page content of the file
     */
    page_content: (string | null);
};
