from flask import Flask, render_template, request
import pymysql




app = Flask(__name__)




# Establish a database connection
def get_connection():
    return pymysql.connect(
        host="127.0.0.1", #localhost
        port=3308,#บรรทัดนี้ไม่มีก็ได้
        user="root",
        password="",
        db="db_northwind"#ชื่อsqlที่เราต้องการดึงข้แมูลกันมา
    )




@app.route("/")
def home():
    try:
        # Connect to the database
        conn = get_connection()




        # Create a cursor
        cursor = conn.cursor()




        # Execute a query
        cursor.execute("SELECT * FROM tb_products")#เลือกcolumชื่อนี้




        # Fetch all rows from the result
        rows = cursor.fetchall()




        # Close the cursor and connection
        cursor.close()
        conn.close()




        # Render the template and pass the rows data to it
        return render_template("index.html", rows=rows)




    except pymysql.Error as e:
        return "Connection failed: " + str(e)#ถ้าเชื่อมไม่ได้ส่งค่ามาแจ้งเตือน


@app.route("/test", methods=["POST"])
def test():
    try:
        # Get the value from the form submission
        result = request.form.get("result")#รอรับค่าจากhome()มาเก็บที่result


        # Connect to the database
        conn = get_connection()


        # Create a cursor
        cursor = conn.cursor()


        # Execute a query to find categoryID based on the result
        cursor.execute("SELECT categoryID FROM tb_products WHERE productName = %s", result)#เอาค่าจากresultที่มีในproductNameมาเทียบtb_productsและส่งค่ากลับมาชื่อตัวแปลเดิม


        # Fetch the categoryID from the result
        category_id = cursor.fetchone()[0]#category_idรอรับค่า


        # Execute a query to find categoryName based on categoryID
        cursor.execute("SELECT categoryName FROM tb_categories WHERE categoryID = %s", category_id)#category_idมาเทียบกับtb_categoriesและส่งกลับมา category_nameที่รอรับค่าอยู่


        # Fetch the categoryName from the result
        category_name = cursor.fetchone()[0]


        # Close the cursor and connection
        cursor.close()
        conn.close()


        # Render the template and pass the result, category_id, and category_name data to it
        return render_template("test.html", result=result, category_name=category_name)#ส่งค่าขึ้นไปที่web


    except Exception as e:
        return "Error: " + str(e)




if __name__ == "__main__":
    app.run()



