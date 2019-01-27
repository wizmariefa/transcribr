import ReactDropzone from "react-dropzone";
import React, { Component } from "react";

export default class TranscribrDropzone extends Component {
    constructor(){
        super();
    }

    render() {
        return (
          <div className="TranscribrDropzone">
            <ReactDropzone onDrop={this.onDrop} >
              Drop your best gator GIFs here!!
            </ReactDropzone>
          </div>
        );
      }
}
