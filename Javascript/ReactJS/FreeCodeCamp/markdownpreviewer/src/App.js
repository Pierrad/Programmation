import React from 'react';
import marked from 'marked';
import './App.css';

const BASICMARKDOWN = `# Header
## Sub Header
[Google](www.google.com)

Code \`<div></div>\`, simple div

\`\`\`
// plusieurs lignes:

function test(){
  console.log("dab");
}
\`\`\`

- List
- List2

> okay

**wow**

![Tux, the Linux mascot](https://images.frandroid.com/wp-content/uploads/2019/09/tesla-model-s-1563301327.jpg)
`

class MarkdownPreviewer extends React.Component{
  constructor(props){
    super(props);
    this.state = {
      editor:BASICMARKDOWN,
      preview:marked(BASICMARKDOWN)
    }
  }

  // Arrow function to bind this
  setPreview = (event) => {
    this.setState({
      editor: event.target.value,
      preview: marked(event.target.value)
    })
  }

  render(){
    return(
      <div className="divContainer">
        <h1>- Markdown Previewer -</h1>
        <textarea id="editor" value={this.state.editor} onChange={this.setPreview} type="text"/>
        <p id="preview">
          <td dangerouslySetInnerHTML={{__html: this.state.preview}}/>
        </p>
      </div>
    );
  }
}

export default MarkdownPreviewer;
