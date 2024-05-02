function SiteRender(site) {
    const htmlCode = `
      <!DOCTYPE html>
      <html>
      <head>
        <style>
          body {
            background-color: lightblue;
          }
          h1 {
            color: white;
          }
        </style>
        <script>
          function myFunction() {
            document.getElementById("demo").innerHTML = "Hello JavaScript!";
          }
        </script>
      </head>
      <body onload="myFunction()">
        <h1 id="demo">Hello, World!</h1>
      </body>
      </html>
    `;
  
    return (
      <iframe srcDoc={site.sourceCode} width="100%" height="100%" />
    );
  }
  
  export default SiteRender;

// function SiteRender() {
//     const htmlCode = `
//       <!DOCTYPE html>
//       <html>
//       <head>
//         <style>
//           body {
//             background-color: lightblue;
//           }
//           h1 {
//             color: white;
//           }
//         </style>
//         <script>
//           function myFunction() {
//             document.getElementById("demo").innerHTML = "Hello JavaScript!";
//           }
//         </script>
//       </head>
//       <body onload="myFunction()">
//         <h1 id="demo">Hello, World!</h1>
//       </body>
//       </html>
//     `;
  
//     return (
//       <iframe srcDoc={htmlCode} width="100%" height="100%" />
//     );
//   }
  
//   export default SiteRender;