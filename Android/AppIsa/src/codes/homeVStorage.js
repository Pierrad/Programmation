getBase64 = async (url) => {
    const fs = RNFetchBlob.fs;
    let imagePath = null;
    let base64 = 64;
    await RNFetchBlob
      .config({
        fileCache: true
      })
      .fetch("GET", url)
      // the image is now dowloaded to device's storage
      .then(resp => {
        // the image path you can use it directly with Image component
        imagePath = resp.path();
        return resp.readFile("base64");
      })
      .then(base64Data => {
        // here's base64 encoded image
        base64 = base64Data.toString();
        // remove the file from storage
        return fs.unlink(imagePath);
      });

    return base64;
  }

  GetData = (Imgnumber, compteur) => {
    this.setState({loading:true})
    let reference = firebase.storage().ref('Test/Image'+ compteur.toString() + '.jpg');
    reference.getDownloadURL()
    .then(url => {
      return this.getBase64(url);
    })
    .then(base => {
      if (base !== null) {
        this.setState({base64:base, allBase: [...this.state.allBase, {id:'Image' + compteur.toString(), src: base}]});
        Imgnumber = Imgnumber - 1;
        compteur = compteur + 1;
        if(Imgnumber>0) {
          this.GetData(Imgnumber, compteur)
        }
        else{
          this.setState({loading:false, disableButton:true});
        }
      }
    });
  }

