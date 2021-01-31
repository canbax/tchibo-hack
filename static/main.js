function getSimilar2() {
  const v = document.getElementById('product-idx').value;
  const xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      const obj = JSON.parse(this.responseText);
      const container = document.getElementById('similar-products');
      container.innerHTML = '';
      for (let i = 0; i < obj.length; i++) {
        generateCard4Product(obj[i].product_data, container, obj[i]);
      }
    }
  };
  xhttp.open('GET', 'similars?product_idx=' + v, true);
  xhttp.send();
}

function getProductInfo() {
  const v = document.getElementById('product-idx').value;
  const xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      const obj = JSON.parse(this.responseText);
      const container = document.getElementById('curr-product');
      container.innerHTML = '';
      generateCard4Product(obj, container);
    }
  };
  xhttp.open('GET', 'product?product_idx=' + v, true);
  xhttp.send();
}

function generateCard4Product(x, container, similarityData) {
  const cardDiv = document.createElement('div');
  cardDiv.style.width = '18rem;'
  cardDiv.className = 'card';
  
  const img = document.createElement('img');
  img.className = 'card-img-top';
  img.src = x.image.default;

  const cardBodyDiv = document.createElement('div');
  cardBodyDiv.className = 'card-body';

  const cardTitle = document.createElement('h5');
  cardTitle.className = 'card-title';
  cardTitle.innerText = x.title;

  const cardText = document.createElement('p');
  cardText.className = 'card-text';
  if ( x.description.long.length > 30) {
    cardText.innerText = x.description.long.substr(0, 27) + '...';  
  } else {
    cardText.innerText = x.description.long;
  }

  cardBodyDiv.appendChild(cardTitle);
  cardBodyDiv.appendChild(cardText);

  const list = document.createElement('ul');
  list.className = 'list-group list-group-flush';

  const listItem = document.createElement('li');
  listItem.className = 'list-group-item';
  listItem.innerText = 'Google Shopping API:' + x.category.google_shopping_api;

  const listItem2 = document.createElement('li');
  listItem2.className = 'list-group-item';
  listItem2.innerText = 'Price:' + x.price.amount;

  list.appendChild(listItem);
  list.appendChild(listItem2);

  if (similarityData) {
    for (let i = 0; i < 3; i++) {
      const li = document.createElement('li');
      li.className = 'list-group-item';
      li.innerText = 'Similarity ' + i + ': ' + similarityData['sim' + i];
      list.appendChild(li);
    }

    const li = document.createElement('li');
    li.className = 'list-group-item';
    li.innerText = 'Recommend Score: ' + similarityData['recommend_score'];
    list.appendChild(li);
  }

  cardDiv.appendChild(img);
  cardDiv.appendChild(cardBodyDiv);
  cardDiv.appendChild(list);

  container.appendChild(cardDiv);
}