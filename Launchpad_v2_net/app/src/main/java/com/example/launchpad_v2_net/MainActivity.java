package com.example.launchpad_v2_net;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    public String message;

    public String File_Names = "";
    public String[] File_Names_array = null;

    TextView tv;

    ImageView KijeloltGomb;
    int Selected_Btn_index = 0;
    ArrayList<ImageView> BTNKeys = new ArrayList<>();

    ArrayList<TextView> textViews = new ArrayList<>();

    String selected_text = "";

    public LinearLayout LL;

    public EditText ipAddress;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        ipAddress = findViewById(R.id.ipAddr);
        LL = findViewById(R.id.linearLayout);
        tv = findViewById(R.id.fileNames);

        BTNKeys.add(findViewById(R.id.BTNKey1));
        BTNKeys.add(findViewById(R.id.BTNKey2));
        BTNKeys.add(findViewById(R.id.BTNKey3));
        BTNKeys.add(findViewById(R.id.BTNKey4));
        BTNKeys.add(findViewById(R.id.BTNKey5));
        BTNKeys.add(findViewById(R.id.BTNKey6));
        BTNKeys.add(findViewById(R.id.BTNKey7));
        BTNKeys.add(findViewById(R.id.BTNKey8));
        BTNKeys.add(findViewById(R.id.BTNKey9));


    }

    public void BTNKey_image_update(ImageView btn){
        for(ImageView gomb : BTNKeys){
            if(gomb != btn){
                gomb.setImageResource(R.drawable.btnkey_base);
            }
        }
    }

    @SuppressLint("NonConstantResourceId")
    public void BTNKey_pressed(View view) {
        ImageView btn = (ImageView)view;
        KijeloltGomb = btn;
        BTNKey_image_update(btn);
        btn.setImageResource(R.drawable.btnkey_pressed);
        if(File_Names.equals("")){
            send sendcode = new send();
            message = "Get_Files";
            sendcode.execute();
        }
        switch(btn.getId()){
            case R.id.BTNKey1:
                Selected_Btn_index = 1;
                break;
            case R.id.BTNKey2:
                Selected_Btn_index = 2;
                break;
            case R.id.BTNKey3:
                Selected_Btn_index = 3;
                break;
            case R.id.BTNKey4:
                Selected_Btn_index = 4;
                break;
            case R.id.BTNKey5:
                Selected_Btn_index = 5;
                break;
            case R.id.BTNKey6:
                Selected_Btn_index = 6;
                break;
            case R.id.BTNKey7:
                Selected_Btn_index = 7;
                break;
            case R.id.BTNKey8:
                Selected_Btn_index = 8;
                break;
            case R.id.BTNKey9:
                Selected_Btn_index = 9;
                break;
        }

        if(!File_Names.equals("") && File_Names_array == null){
            File_Names_array = File_Names.split("@");
            int i = 0;
            for(String szoveg : File_Names_array){
                textViews.add(new TextView(MainActivity.this));
                textViews.get(i).setText(szoveg);
                textViews.get(i).setTextSize(30);
                textViews.get(i).setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View view) {
                        textClicked(view);
                    }
                });
                textViews.get(i).setTextColor(getResources().getColor(R.color.purple_200));
                LL.addView(textViews.get(i));
                i++;
            }
        }
    }

    public void textClicked(View view) {
        TextView textView = (TextView) view;
        selected_text = textView.getText().toString();
        Toast.makeText(MainActivity.this, selected_text, Toast.LENGTH_SHORT).show();
        StringBuilder stringBuilder = new StringBuilder();
        stringBuilder.append(Selected_Btn_index);
        stringBuilder.append("@");
        stringBuilder.append(selected_text);
        send sendcode = new send();
        message = stringBuilder.toString();
        sendcode.execute();
    }

    public void dc_button_pressed(View view) {
        send sendcode = new send();
        message = "!DC";
        sendcode.execute();
    }

    class send extends AsyncTask<Void,Void,Void> {
        Socket s;
        PrintWriter pw;
        @Override
        protected Void doInBackground(Void...params){
            try {
                s = new Socket(ipAddress.getText().toString(),8000);
                pw = new PrintWriter(s.getOutputStream());
                pw.write(message);
                pw.flush();
                if(message.equals("Get_Files")) {
                    BufferedReader in = new BufferedReader(new InputStreamReader(
                            s.getInputStream()));
                    File_Names = in.readLine();
                    System.out.println(File_Names);
                    in.close();
                }
                pw.close();

                s.close();
                System.out.println(message);
            } catch (UnknownHostException e) {
                System.out.println("Fail");
                e.printStackTrace();
            } catch (IOException e) {
                System.out.println("Fail");
                e.printStackTrace();
            }
            return null;
        }
    }

}

















