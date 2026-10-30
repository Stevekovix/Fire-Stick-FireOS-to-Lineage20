package local.androidtv.shortcuts;
import android.accessibilityservice.AccessibilityService;
import android.content.Intent;
import android.view.KeyEvent;
import android.view.accessibility.AccessibilityEvent;
import android.util.Log;
import android.widget.Toast;
public final class ShortcutService extends AccessibilityService {
 public void onAccessibilityEvent(AccessibilityEvent e) {}
 public void onInterrupt() {}
 protected void onServiceConnected() { Log.i("TvShortcuts","Service ready"); }
 protected boolean onKeyEvent(KeyEvent e) {
  int index=e.getKeyCode()==KeyEvent.KEYCODE_F12 ? 3 : e.getKeyCode()-KeyEvent.KEYCODE_BUTTON_1;
  if(index<0 || index>3)return false;
  String[] packages={"com.netflix.ninja","com.amazon.amazonvideo.livingroom","com.disney.disneyplus","com.amazon.music.tv"};
  if(e.getAction()==KeyEvent.ACTION_DOWN && e.getRepeatCount()==0) {
   String p=packages[index];
   Intent i=new Intent(Intent.ACTION_MAIN).addCategory("android.intent.category.LEANBACK_LAUNCHER").setPackage(p);
   java.util.List<android.content.pm.ResolveInfo> matches=getPackageManager().queryIntentActivities(i,0);
   if(!matches.isEmpty()) {
    android.content.pm.ActivityInfo a=matches.get(0).activityInfo;
    i.setComponent(new android.content.ComponentName(a.packageName,a.name));
   } else i=null;
   if(i==null)i=getPackageManager().getLaunchIntentForPackage(p);
   if(i==null){Toast.makeText(this,"Aucun écran de lancement trouvé",Toast.LENGTH_SHORT).show();return true;}
   i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK|Intent.FLAG_ACTIVITY_RESET_TASK_IF_NEEDED);
   try { startActivity(i);Log.i("TvShortcuts","Launched "+p+" key="+e.getKeyCode()); }
   catch(RuntimeException x){Log.e("TvShortcuts","Launch failed for "+p,x);}
  }
  return true;
 }
}
