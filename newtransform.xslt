<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <!-- Template to match the root element -->
    <xsl:template match="/Books">
        <html>
            <head>
                <title>Book Quest</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css"
                    rel="stylesheet"
                    integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC"
                    crossorigin="anonymous" />
                <style>
                    .container{
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        width: 80%;
                        padding: 16px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h2 class="h2 py-3">Book Quest</h2>
                    <div class="table-responsive">
                        <table class="table align-middle table-hover">
                            <!-- <tr>
                                <th>Image</th>
                                <th>Details</th>
                            </tr> -->
                            <xsl:for-each select="item">
                                <tr>
                                    <td>
                                        <img class="rounded">
                                            <xsl:attribute name="src">
                                                <xsl:value-of select="image_url" />
                                            </xsl:attribute>
                                            <xsl:attribute name="alt">
                                                <xsl:value-of select="title" />
                                            </xsl:attribute>
                                        </img>
                                    </td>
                                    <td>
                                        <p  class="h3">
                                            <xsl:value-of select="title" />
                                        </p>
                                        <p class="h4">
                                           By <xsl:value-of select="authors" />
                                        </p>
                                        <p>
                                            <xsl:value-of select="average_rating" /> / 5
                                        </p>
                                        <p>
                                            Published in <xsl:value-of select="publication_year" />
                                        </p>
                                        <p>
                                            Search Relevance : <xsl:value-of select="score" />
                                        </p>
                                    </td>
                                </tr>
                            </xsl:for-each>
                        </table>
                    </div>
                </div>
                <script
                    src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"
                    integrity="sha384-IQsoLXl5PILFhosVNubq5LC7Qb9DXgDA9i+tQ8Zj3iwWAwPtgFTxbJ8NT4GN1R8p"
                    crossorigin="anonymous"></script>
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.min.js"
                    integrity="sha384-cVKIPhGWiC2Al4u+LWgxfKTRIcfu0JTxR+EQDz/bgldoEyl4H0zUF0QKbrJ0EcQF"
                    crossorigin="anonymous"></script>
            </body>
        </html>
    </xsl:template>

</xsl:stylesheet>