import bot from "../icons/bot.png";
import user from "../icons/user.png";

import styles from "./Message.module.css";

export default function Message({ role, content }) {
  return (
    <div className={styles.wrapper}>
      <div>
        <img
          src={role === "assistant" ? bot : user}
          className={styles.avatar}
          alt="profile avatar"
        />
      </div>
      <div>
        {content.split('\n').map((line, index) => (
          <p key={index}>{line}</p>
        ))}
      </div>
    </div>
  );
}
