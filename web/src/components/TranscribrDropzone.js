import Dropzone from "react-dropzone";
import React, { Component } from "react";
import "./../styles/TranscribrDropzone.scss";

export default class TranscribrDropzone extends Component {
  constructor(){
      super();
  }
  render() {
    return (
      <div className="TranscribrDropzone">
        <Dropzone accept={""} onDrop={files => this.onDrop(files, () => {})}>
          {({ getRootProps, getInputProps, open }) => {
            return (
              <div className="DropzoneContainer" width={this.props.width}>
                <div className="Dropzone" onClick={() => open()} {...getRootProps()}>
                  <input {...getInputProps()} />
                  <div className="Text">
                    Drag or drop files here.
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
