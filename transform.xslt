<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <!-- Template to match the root element -->
    <xsl:template match="/Books">
        <html>
            <head>
                <title>Books Information</title>
                <style>
                    table {
                        border-collapse: collapse;
                        width: 100%;
                    }
                    th, td {
                        border: 1px solid black;
                        padding: 8px;
                        text-align: left;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                </style>
            </head>
            <body>
                <h2>Books Information</h2>
                <table>
                    <tr>
                        <th>Authors</th>
                        <th>Average Rating</th>
                        <th>Book ID</th>
                        <th>Image</th>
                        <th>Publication Year</th>
                        <th>Title</th>
                    </tr>
                    <xsl:for-each select="item">
                        <tr>
                            <td><xsl:value-of select="authors"/></td>
                            <td><xsl:value-of select="average_rating"/></td>
                            <td><xsl:value-of select="book_id"/></td>
                            <td>
                                <img>
                                    <xsl:attribute name="src">
                                        <xsl:value-of select="image_url"/>
                                    </xsl:attribute>
                                    <xsl:attribute name="alt">
                                        <xsl:value-of select="title"/>
                                    </xsl:attribute>
                                </img>
                            </td>
                            <td><xsl:value-of select="publication_year"/></td>
                            <td><xsl:value-of select="title"/></td>
                        </tr>
                    </xsl:for-each>
                </table>
            </body>
        </html>
    </xsl:template>

</xsl:stylesheet>
