/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { FileType } from './FileType';
/**
 * File upload model for user file uploads
 */
export type FileUpload = {
    /**
     * Entity that the file is associated with
     */
    entity_id: string;
    /**
     * File name specified by the user
     */
    title: string;
    /**
     * File upload FastAPI object
     */
    file: Blob;
    /**
     * File type
     */
    file_type: FileType;
    /**
     * File description
     */
    description: (string | null);
};
