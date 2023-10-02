import frappe

from frappe import auth



@frappe.whitelist( allow_guest=True )

def login(usr, pwd):

    try:

        login_manager = frappe.auth.LoginManager()

        login_manager.authenticate(user=usr, pwd=pwd)

        login_manager.post_login()

    except frappe.exceptions.AuthenticationError:

        frappe.clear_messages()

        frappe.local.response["message"] = {

            "success_key":0,

            "message":"Authentication Error!"

        }



        return



    api_generate = generate_keys(frappe.session.user)

    user = frappe.get_doc('User', frappe.session.user)



    frappe.response["message"] = {

        "success_key":1,

        "message":"Authentication success",

        "sid":frappe.session.sid,

        "api_key":user.api_key,

        "api_secret":api_generate,

        "username":user.username,

        "email":user.email

    }







def generate_keys(user):

    user_details = frappe.get_doc('User', user)

    api_secret = frappe.generate_hash(length=15)



    if not user_details.api_key:

        api_key = frappe.generate_hash(length=15)

        user_details.api_key = api_key



    user_details.api_secret = api_secret

    user_details.save()



    return api_secret

@frappe.whitelist(allow_guest=True)

def insert_in(email,lat,lng,imei_no):
    print("******************************************************")
    print(email)
    print(lat)
    print(lng)
    #print(imei_no)
    frappe.db.sql(""" UPDATE `tabEmployee` SET latitude=%s,longitude=%s,imei_no=%s  where user_id=%s """,(lat,lng,imei_no,email))
    frappe.db.commit()
    res = frappe.response["message"] = {

        "success": 1,
        "message": "Location updated successfully"




    }
    return res

@frappe.whitelist(allow_guest=True)

def new_record(email,lat,lng,imei_no):


     # doc = frappe.get_doc(dict(
     #                         doctype = "ImeiLocation",
     #                         email = email,
     #                         latitude = lat,
     #                         longitude = lng,
     #                         imei_no = imei_no
                            
     #                     )).insert(ignore_permissions = True)
     new_record = frappe.new_doc('ImeiLocation')
     new_record.email = email
     new_record.lat = lat
     new_record.lng = lng
     new_record.imei_no = imei_no
     print("********************",email,lat,lng,imei_no)
     new_record.insert(ignore_permissions=True)
     frappe.db.commit
     print("New record******************", new_record)
     result = frappe.response["message"] = {
     "success": 1,
     "message": "Location updated successfully"
     }
     # return result



def update_conversion_factor(doc,event):
    if doc.attributes and doc.variant_of:
        for row in doc.attributes:
            if row.get('attribute') == 'Height':
                doc.height = int(row.get('attribute_value'))
            if row.get('attribute') == 'Width':
                doc.width = int(row.get('attribute_value'))
           if row.get('attribute') == 'Yield':
               doc.yield_ == float(row.get('attribute_value'))

    if not doc.has_variants:
       update_uoms_conversion(doc)


def update_uoms_conversion(doc):
    doc_ = doc.as_dict()
    for row in doc.uoms:
        #if row in doc.uoms:
        if row.formula:
            print(row.as_dict())
            row.conversion_factor = eval(str(row.formula))
            # print("*******************************************************")
            # print(doc_, doc_.height)
            # print(row.formula)
            # print(str(row.formula))
            #row.conversion_factor = eval(str(row.formula), {'doc': frappe._dict({'length': doc.length,'width': doc.width, 'height': doc.height })})





