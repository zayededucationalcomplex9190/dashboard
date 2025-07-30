import pandas as pd
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def main_menu():
    return render_template('main_menu.html')

@app.route('/student')
def student_menu():
    return render_template('student_menu.html')

@app.route('/staff_login', methods=['GET', 'POST'])
def staff_login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'teacher' and password == '12345':
            return redirect(url_for('staff_menu'))
        else:
            error = 'اسم المستخدم أو كلمة المرور غير صحيحة'
    return render_template('staff_login.html', error=error)

@app.route('/staff')
def staff_menu():
    return render_template('staff_menu.html')

@app.route('/view_pdf/<filename>')
def view_pdf(filename):
    title = request.args.get('title', filename)
    return render_template('viewer.html', filename=filename, display_title=title)

@app.route('/report', methods=['GET', 'POST'])
def report():
    student_data = None
    subjects = []
    error = None

    # قائمة أسماء المواد حسب الترتيب
    subject_names = [
        "اللغة العربية",
        "اللغة الإنجليزية - English",
        "التربية الإسلامية",
        "الرياضيات - Math",
        "العلوم - Science",
        "الدراسات الاجتماعية",
        "التصميم والتكنولوجيا - DT",
        "الأحياء - Biology",
        "الفيزياء - Physics",
        "الكيمياء - Chemistry"
    ]

    if request.method == 'POST':
        student_id = request.form.get('student_id', '').strip()
        if not student_id:
            error = 'يرجى إدخال رقم الهوية.'
        else:
            try:
                df = pd.read_excel('students.xlsx').fillna('-')
                df.columns = df.columns.str.strip()
                print("الأعمدة المتوفرة:", df.columns.tolist())

                match = df[df['رقم الهوية'].astype(str) == str(student_id)]
                if not match.empty:
                    student_data = match.to_dict(orient='records')[0]

                    # استخراج بيانات المواد ديناميكيًا
                    for i, name in enumerate(subject_names, start=1):
                        if f'Subject{i}_Formative' in student_data:
                            subject = {
                                'name': name,
                                'formative': student_data.get(f'Subject{i}_Formative', '-'),
                                'academic': student_data.get(f'Subject{i}_Academic', '-'),
                                'participation': student_data.get(f'Subject{i}_Participation', '-'),
                                'alef': student_data.get(f'Subject{i}_Alef', '-'),
                                'behavior': student_data.get(f'Subject{i}_Behavior', '-'),
                                'commitment': student_data.get(f'Subject{i}_Commitment', '-'),
                            }
                            subjects.append(subject)
                else:
                    error = 'الطالب غير موجود في البيانات.'
            except Exception as e:
                error = f"خطأ في قراءة الملف: {e}"

    return render_template('report.html', student=student_data, subjects=subjects, error=error)

if __name__ == '__main__':
    app.run(debug=True)
