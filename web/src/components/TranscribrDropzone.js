import Dropzone from "react-dropzone";
import React, { Component } from "react";
import "./../styles/TranscribrDropzone.scss";
import client from './../util/client';

export default class TranscribrDropzone extends Component {
  uploadFiles(files) {
    console.log(files[0])
    client.uploadFiles(files[0])
    .then(res => console.log(res))
    .catch(err => console.error(err));
  }
  render() {
    return (
      <div className="TranscribrDropzone">
        <Dropzone accept={""} onDrop={files => this.uploadFiles(files)}>
          {({ getRootProps, getInputProps, open }) => {
            return (
              <div className="DropzoneContainer" width={this.props.width}>
                <div className="Dropzone" onClick={() => open()} {...getRootProps()}>
                  <input {...getInputProps()} />
                  <div className="Text">
                    DRAG OR DROP AUDIO FILES HERE
                  </div>
                </div>
              </div>
            )
          }}
        </Dropzone>
      </div>
    );
  }
}
