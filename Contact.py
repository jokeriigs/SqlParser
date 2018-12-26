class Contact:
    name = ""
    phone_number = ""
    e_mail = ""
    addr = ""

    def __init__(self, pname, pphone_number, pe_mail, paddr):
        self.name = pname
        self.phone_number = pphone_number
        self.e_mail = pe_mail
        self.addr = paddr


class Contact_Mgr:

    Contact_list = []
    
    def print_contact(self,pf, pname):
        for contact in self.Contact_list:
            if pf == 'A' or contact.name == pname:
                print("이름 : " + contact.name)
                print("전화번호 : " + contact.phone_number)
                print("이메일 : " + contact.e_mail)
                print("주소 : " + contact.addr)
                print("")       

    def print_menu(self):
        print("1. 연락처 입력")
        print("2. 연락처 출력")
        print("3. 연락처 삭제")
        print("4. 종료")
        menu = input("메뉴선택: ")
        return int(menu)

    def input_Contact(self):
        name = ""
        phone_number = ""
        e_mail = ""
        addr = ""

        name = input('이름을 입력하세요 : ')
        phone_number = input('전화번호를 입력하세요 : ')
        e_mail = input('이메일을 입력하세요 : ')
        addr = input('주소를 입력해주세요 : ')
        
        self.Contact_list.append(Contact(name, phone_number, e_mail, addr))
        
        print('입력이 완료되었습니다.')

    def del_Contact(self, pf):
         for contact in self.Contact_list:
            if pf == 'A':
                self.Contact_list.clear()
            else:
                for contact in self.Contact_list:
                    if contact.name == pf:
                        self.Contact_list.remove(contact)

    def run(self):
        pf = ""
        while 1:
            menu = self.print_menu()
            if menu == 1:
                self.input_Contact()
            elif menu == 2:
                pf = input("출력할 주소록을 입력해주세요(A:모두 출력) : ")
                if pf == 'A':
                    self.print_contact(pf, '')
                else:
                    self.print_contact('', pf)
            elif menu == 3:
                pf = input("삭제할 주소록을 입력해주세요(A:모두 삭제) : ")
                self.del_Contact(pf)   
            elif menu == 4:
                break
            

contact_mgr = Contact_Mgr()
contact_mgr.run()